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
document is going to contain all of the content on this page.

# Implementation 

Let's try this out by ourselves 
**Preparing the data** - Let's say we have a big document, we are going to split the document into smaller chunks. A chunk could be a paragraph, a sentence or several pages. By doing this, the outcome that we are looking for when we search through all of this data, each chunk is going to be more focused and more relevant.To achieve this we used a recursive character text splitter. We made the chunk size to be a 1000 characters and each chunk is going to have an overlap of 500 characters.

**Creating Chroma Database** - To be able to query each chunk, we are going to need to turn this into a database.

![DB](/database.png)

**Vector Embedding** - Embeddings are vector representations of text that capture their meaning. In python, this is literally a list of numbers. They can be thought of as coordinates in multidimensional space. If two pieces of text are closely related to each other in meaning, then these coordinates will also be close together.
The distance between these vectors can then be calculated using cosine similarity or euclidean distance.

![VE](/vector_embeddings.png)

**Querying** - To query for relevant data, our objective is to find the chunks in our database that will most likely contain the answer to the question that we want to ask. So our goal now is to take a query, then turn that into an embedding using an embedding function and then scan through our database and find, say, 5 chunks of information that closest in embedding distance from our query. From here, we can put them together and have the model that we are using read all of that information and decide the response to show the user.

![Q](/querying.png)

**Creating a response** - We will create a prompt template to create a prompt with. Prompt will contain the context that we pass in. The context would be the pieces of information that we got from the database and the actual query.
