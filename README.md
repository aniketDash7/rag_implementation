# RAG
We need to pick a model and at the moment it feels like all the good models are based on "meta-llama", so we will pick "meta-llama/Llama-2-7b-hf".
According to the ULMFiT approach the llama-2 ( 7 billion ) has only been upto to the LM-Pretraining phase, it has done none of the fine tuning or instruction tuning. 
We will implement a framework to help large language model be more accurate and upto date. This is called Retrieval Augmented Generation ( RAG ) 
Let's talk about the generation part for now 
# Generation 
In the context of LLMs generation refers to generate text in response to an user query, referred to as prompt. These models can have some undesirable behaviour. 
There are two problematic things about this : 
- No sources
- Out of date information
So to tackle this issue instead of entirely relying on LLM for information we are adding a content store. The content store could be open like the internet or closed like some collection of documents,collection of policies. So when the query is encountered by the LLM, it first goes to the content store and asks about the query.
To formally put it we can mention the steps here :
- User prompts the LLM with their question
- With RAG, The LLM is given an instruction to retrieve relevant information or content and combine with the user query and then generate the answer.
How does RAG help with the challenges LLM faces ?
1. Instead of having to retrain the model, if new information comes up, all you have to do is augment your datastore with new information.
2. LLM is now instructed to pay attention to primary source data before giving out the response. This makes it less likely to hallucinate because it is less likely to rely on information that it learned during its training.
