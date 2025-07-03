from my_agent.common.agent import ChainAGent
from langgraph.graph.state import CompiledStateGraph
from langgraph.graph import StateGraph, START
from my_agent.agents.rag_agent.nodes.retriever import RetrieverNode
from my_agent.agents.rag_agent.nodes.embedder import EmbedderNode
from my_agent.agents.rag_agent.nodes.ranker import RankerNode
from my_agent.agents.rag_agent.nodes.generator import GeneratorNode
from my_agent.agents.rag_agent.nodes.preprocessor import PreprocessorNode

class RAGAgent(ChainAGent):
    def __init__(self, model=None, prompt_path='/home/yuqi/langgraph/demo/my_agent/agents/rag_agent/prompts.txt'):
        retriever_node = RetrieverNode(knowledge_base=None)
        embedder_node = EmbedderNode(embedding_model=None)
        ranker_node = RankerNode(ranking_model=None)
        generator_node = GeneratorNode(generation_model=None)
        preprocessor_node = PreprocessorNode()
        
        nodes = [
            retriever_node,
            embedder_node,
            ranker_node,
            generator_node,
            preprocessor_node
        ]
        super().__init__(model, prompt_path, nodes, name="RAGAgent")
