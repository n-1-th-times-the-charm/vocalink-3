import logging
from typing_extensions import TypedDict
from time import sleep
import traceback
from agent.constants import FILE_PATH
from agent.agents import modify_agent, execute_agent
from langgraph.graph import StateGraph, START, END
from nltk.tokenize import sent_tokenize
from agent.utils import get_expert

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("vocalink")

try:
    file = open(FILE_PATH, "a+")
    file.seek(0)
    logger.info(f"Successfully opened file at {FILE_PATH}")
except Exception as e:
    logger.error(f"Failed to open file at {FILE_PATH}: {str(e)}")
    raise

class State(TypedDict):

    """

        TypedDict to represent the state in the LangGraph flow.
        
        Attributes:

            user_input (str): The latest transcription provided by the user.
            current_file_state (str): The current state of the entire file content.

    """

    user_input: str
    current_file_state: str
    
def router(state: State) -> str:
    """

        Routes the user input to the appropriate expert based on the content.
        This function analyzes the user input and determines which expert should handle
        the request, returning the name of the appropriate handler function.
        
        Args:

            state (State): The current LangGraph state containing user input and file state.

        Returns:

            str: The name of the expert function to route to.

    """

    try:
        logger.info(f"Routing user input: '{state['user_input'][:50]}...'")
        result = get_expert(state["user_input"])
        expert = result
        logger.info(f"Routed to expert: {expert}")
        return "execute"
    except Exception as e:
        logger.error(f"Error during routing: {str(e)}")
        logger.debug(traceback.format_exc())
        return "transcribe"
    
def process_input(state: State) -> dict:

    """

        Preprocesses the user input by stripping leading and trailing whitespaces.
        
        Args:
        
            state (State): The current LangGraph state.

        Returns:

            dict: Updated state with processed user input.

    """

    try:
        text = state["user_input"]
        processed_text = text.strip()
        logger.info(f"Processed input: '{processed_text[:50]}...'")
        return {
            "user_input": processed_text
        }
    except Exception as e:
        logger.error(f"Error during input processing: {str(e)}")
        logger.debug(traceback.format_exc())
        return {
            "user_input": state["user_input"]
        }

def modify(state: State) -> dict:

    """

        Modifies the file content by deleting the last two sentences and appending new content.
        This function removes the last two sentences from the file content, then uses the
        modify_agent to generate new content based on the user input and context. The new
        content is appended to the modified file.
        
        Args:

            state (State): The current LangGraph state.

        Returns:

            dict: Updated state with the new file content.

    """

    logger.info("Starting modify function")
    current_text = state["current_file_state"]
    user_input = state["user_input"]
    logger.info(f"Current text (first 100 chars): {current_text[:100]}...")
    
    try:
        sentences = sent_tokenize(current_text)
        logger.info(f"Found {len(sentences)} sentences")
        if len(sentences) >= 2:
            context = " ".join(sentences[-2:])
        else:
            context = current_text
        logger.info(f"Using context: '{context[:100]}...'")
        output = ""
        if len(sentences) >= 2:
            joined_text = " ".join(sentences[:-2])
            new_length = len(joined_text)
            file.seek(new_length)
            file.truncate()
            file.seek(new_length)
            logger.info(f"Truncated file to {new_length} characters")
        else:
            file.seek(0)
            file.truncate()
            file.seek(0)
            logger.debug("File cleared - no sentences to delete")
            joined_text = ""
        logger.info("Input: " + user_input)
        logger.info("Context: " + context)
        logger.info("Streaming from modify_agent")
        try:
            for chunk in modify_agent.stream({"input": user_input, "state": context}):
                file.write(chunk.content)
                output += chunk.content
                file.flush()
                logger.info(f"Received chunk: '{chunk.content[:50]}...'")
        except Exception as agent_error:
            logger.error(f"Error during modify_agent streaming: {str(agent_error)}")
            logger.debug(traceback.format_exc())
        if len(sentences) >= 2:
            sliced_sentences = sentences[:-2]
            joined_text = " ".join(sliced_sentences)
            new_text = joined_text + ' ' + output
        else:
            new_text = output
        logger.info(f"Modify complete, new text length: {len(new_text)}")
        return {
            "current_file_state": new_text
        }
    except Exception as e:
        logger.error(f"Error in modify function: {str(e)}")
        logger.debug(traceback.format_exc())
        return {
            "current_file_state": current_text
        }
    
def execute(state: State) -> dict:

    """

        Executes a complete rewrite of the file based on user input and current state.
        This function replaces the entire file content with new content generated by the
        execute_agent based on the user input and current file state.
        
        Args:

            state (State): The current LangGraph state.

        Returns:

            dict: Updated state with the new file content.

    """

    logger.info("Starting execute function")
    current_text = state["current_file_state"]
    user_input = state["user_input"]
    output = ""
    
    try:
        file.seek(0)
        file.truncate()
        logger.info("File cleared for execution")
        logger.info("Streaming from execute_agent")
        try:
            for chunk in execute_agent.stream({"input": user_input, "state": current_text}):
                file.write(chunk.content)
                logger.info(f"Received chunk: '{chunk.content[:50]}...'")
                output += chunk.content
                file.flush()
        except Exception as agent_error:
            logger.error(f"Error during execute_agent streaming: {str(agent_error)}")
            logger.debug(traceback.format_exc())
        new_text = output
        logger.info(f"Execute complete, new text length: {len(new_text)}")
        return {
            "current_file_state": new_text
        }
    except Exception as e:
        logger.error(f"Error in execute function: {str(e)}")
        logger.debug(traceback.format_exc())
        return {
            "current_file_state": current_text
        }
    
def transcribe(state: State) -> dict:

    """

        Transcribes the user input directly to the file, word by word.
        This function writes the user input to the file one word at a time with a small
        delay between words to simulate transcription. It then reads the file contents
        to update the state.
        
        Args:

            state (State): The current LangGraph state.

        Returns:
        
            dict: Updated state with the current file content.

    """

    logger.info("Starting transcribe function")
    try:
        words = state["user_input"].split()
        logger.debug(f"Transcribing {len(words)} words")
        
        for word in words:
            file.write(word + " ")
            sleep(0.1)
            file.flush()
        file.seek(0)
        current_text = file.read()
        logger.info(f"Transcription complete, file length: {len(current_text)}")
        return {
            "current_file_state": current_text
        }
    except Exception as e:
        logger.error(f"Error in transcribe function: {str(e)}")
        logger.debug(traceback.format_exc())
        return {
            "current_file_state": state.get("current_file_state", "")
        }
    
try:
    logger.info("Building VocaLink StateGraph")
    vocalink = StateGraph(State)
    vocalink.add_node("process_input", process_input)
    vocalink.add_node("modify", modify)
    vocalink.add_node("execute", execute)
    vocalink.add_node("transcribe", transcribe)
    vocalink.add_edge(START, "process_input")
    vocalink.add_conditional_edges("process_input", router)
    vocalink.add_edge("modify", END)
    vocalink.add_edge("execute", END)
    vocalink.add_edge("transcribe", END)
    vocalink_graph = vocalink.compile()
    logger.info("VocaLink StateGraph compiled successfully")
except Exception as e:
    logger.critical(f"Failed to build StateGraph: {str(e)}")
    logger.debug(traceback.format_exc())
    raise