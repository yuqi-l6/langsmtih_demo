from abc import ABC, abstractmethod
from langgraph.graph.state import CompiledStateGraph
from langgraph.graph import StateGraph, START
from my_agent.common.state import State

class Agent(ABC):
    def __init__(self, model, prompt_path):
        self.model = model
        self.prompt = self.load_prompt(prompt_path)

    def load_prompt(self, prompt_path):
        try:
            with open(prompt_path, 'r') as file:
                return file.read()
        except FileNotFoundError:
            raise ValueError(f"Prompt file not found: {prompt_path}")
        except Exception as e:
            raise ValueError(f"Error loading prompt file: {e}")
        
    @abstractmethod
    def create_workflow(self):
        """
        Create the workflow for the agent.
        This method should be implemented by subclasses to define the specific workflow.
        """
        pass    


class ChainAGent(Agent):
    def __init__(self, model, prompt_path, configured_nodes, name):
        super().__init__(model, prompt_path)
        self.configured_nodes = configured_nodes
        self.name = name

    def create_workflow(self):
        """
        Create the workflow for the ChainAgent.
        This method should define the specific workflow for the ChainAgent.
        """
        # Implement the workflow creation logic here
        graph_builder = StateGraph(State)
        node_sequence = []
        for i, node in enumerate(self.configured_nodes):
            node_name = f"node_{i}"
            node_sequence.append((node_name, node))
        graph_builder.add_sequence(node_sequence)
        graph_builder.set_entry_point("node_0")        
        return graph_builder.compile(name=self.name)