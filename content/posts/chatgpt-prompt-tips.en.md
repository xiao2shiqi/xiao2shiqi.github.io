+++
date = '2023-06-05T14:39:11+08:00'
draft = false
title = 'Prompt Engineering Tips for Large Language Models'
tags = ["Artificial Intelligence"]
+++

### Overview

Some time ago, I took a course on Prompts at [DeepLearning.ai](https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers/). I found it very beneficial, so I'm summarizing and sharing my learning notes here, hoping to help everyone.

![www.deeplearning.ai](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/ebd45af3fb8640619ea06d2caa519a2c~tplv-k3u1fbpfcp-zoom-1.image)

Why learn Prompts?

Because in the future `AIGC` era, learning effective `Prompt` cues to effectively utilize AI to complete repetitive work will be one of the essential skills for everyone.

The following is my personal summary after completing this course:

1. **Better task completion**: Imagine if you give AI a vague question, you will only get a vague answer.
2. **Diversified results**: You can let AI produce results in more dimensions, not limited to: code, JSON, XML, HTML, and other formatted text, or even images, videos, etc.
3. **Avoid AI limitations**: AI likes to fabricate facts, which is a known flaw of current AI. However, effective Prompts can help you effectively avoid this known, but currently unsolvable, flaw.
4. **No more belief in perfect Prompts**: After learning the truth, you will no longer believe in various so-called "magic" or "fast-track training guides" like [awesome-chatgpt-prompts-zh](https://github.com/PlexPt/awesome-chatgpt-prompts-zh), **because there is no such thing as a perfect Prompt**.
5. **Understand AI capabilities**: Current large model capabilities are limited to: summarization, reasoning, conversion, expansion, etc. Current AI is not omnipotent; don't over-mythologize it, but don't over-belittle it either.

In short, learning Prompts can help you better interact with LLM models, guide them to generate text that meets your needs, and improve efficiency and accuracy. I also recommend that you watch the full video course if you have time. I won't go into too much detail. Below are my learning notes for the course.

### Chapter 1: Introduction

The first chapter mainly introduces several basic principles to follow when communicating with `ChatGPT` or similar `LLMs`:

1. **Clear instructions**: Clear instructions yield more accurate replies. For example, instead of asking "What should I eat?", you can ask "What protein sources should I add to a vegetarian diet?".
2. **Reasonable expectations**: The knowledge base of a model is related to its training parameters and direction. For example, for a general large model like `ChatGPT`, it cannot provide accurate answers for particularly complex problems that require deep professional knowledge. **Specific domain problems must be solved by specialized models for those domains**.
3. **Verify results**: As mentioned above, for particularly complex and professional questions, AI sometimes fabricates information. You must verify the AI's response; if you find an error, try asking in a different way.
4. **Allow time for AI to think**: AI needs to understand your question and generate a useful response, which may take some time, especially for complex questions. Have a little patience.

These are the basic principles for asking AI in the first chapter of the course. Hope it helps.

### Chapter 2: Guidelines

Chapter 2 mainly introduces the following content:

1. How to use ChatGPT for structured output, such as JSON, HTML, XML, etc.
2. How to use Prompts to effectively avoid the problem of AI fabricating facts (as mentioned above).

#### Generating Structured Data

In common scenarios such as data processing and analysis, and API development and testing, you may need to generate or parse JSON data. You can use ChatGPT to help you complete these tasks.

For example, if we want ChatGPT to generate a JSON object containing someone's information, we can ask in the following way:

**Command**: "Please generate a JSON object containing a name (John Doe), age (30), and profession (Software Engineer)."

ChatGPT might generate the following output:

```json
{
    "name": "John Doe",
    "age": 30,
    "profession": "Software Engineer"
}
```

This is a basic example; you can customize the properties and values as needed. It's even very simple to have it generate a virtual JSON array object.

#### How to Avoid AI Fabricating Facts?

ChatGPT is a language model trained on a large amount of text. Therefore, it may generate answers containing incorrect, outdated, or guessed information.

However, by optimizing your questions or prompts, you can reduce this possibility. The methods are as follows:

1. **Ask for sources**: When asking for factual information, ask the model to cite its information sources. (Currently, GPT-4 has implemented internet-connected functions).
2. **Seek explanations rather than facts**: If you want to understand a specific concept or theory, consider seeking an explanation for it rather than a specific fact. For example, asking "What is deep learning?" might get a more accurate answer than asking "What is the most important research in deep learning?", as the latter might lead the model to guess or fabricate.
3. **Use multiple questions**: If you are unsure about the answer to a question, try repeating the question in different ways, or ask the model to explain its answer. This can help you understand the problem from different angles and may reveal inaccuracies in the model.

Example:

Suppose you want to know how a battery works, you can ask in the following way:

**Direct question**: "How does a battery work?"

In response, ChatGPT might give a basic answer explaining the chemical reactions and energy conversion in a battery.

However, you might want a more detailed answer or to verify the model's answer. You can improve your question in the following way:

**Seek a detailed explanation**: "Can you explain in detail how a battery works, specifically how chemical reactions produce current?"

This question asks the model to provide a more detailed answer and focuses on a specific aspect of the battery. Furthermore, you can ask the model to cite its information sources:

**Ask for sources**: "Can you explain in detail how a battery works, specifically how chemical reactions produce current? And please provide your information sources."

Such a question can lead the model to generate a more complete and detailed answer, and provide sources derived from its training data as much as possible.

Finally, if you have doubts about the model's answer, you can repeat the question in different ways or ask the model to explain its answer:

**Use multiple questions and ask for an explanation**: "Can you explain how the chemical reactions inside a battery produce current? How is it converted into the electricity we use? What scientific principles is your answer based on?"

This way of asking not only helps understand the problem from different angles but also challenges the model's answer, checking if it is based on sound scientific principles.

### Chapter 3: Iterative

This chapter mainly explains how to let AI solve problems better through sufficient iterations (context and environment). This is what Andrew Ng meant by **don't believe in perfect Prompts**. Simple Prompts can only solve simple problems; only sufficient iterations (context and environment) can truly solve the problem you are currently facing. The main reasons are as follows:

1. **Understand the full picture of the problem**: Providing more context can help ChatGPT better understand your question. For example, if you just simply ask "How big is it?", ChatGPT cannot know what you are asking about. But if you first say "I just bought a new mobile phone," and then ask "How big is it?", ChatGPT will understand that you are asking about the size of the phone.
2. **Eliminate ambiguity**: Context can help eliminate language ambiguity. Many words and phrases can have different meanings in different contexts. If you provide enough context, ChatGPT can better understand what you mean.
3. **Understand the background of the problem**: In some cases, understanding the background information of the problem is important for generating useful answers.
4. **Track conversation coherence**: In an ongoing conversation, providing context can help ChatGPT maintain conversation coherence.

Overall, providing more context information can help ChatGPT answer your questions more accurately and usefully. This is also why we say don't believe in perfect Prompts.

### Chapter 4: Summarizing

This chapter mainly introduces ChatGPT's ability to summarize redundant information. In an era of information explosion and fast pace, it is almost impossible to read an entire academic masterpiece, or a lengthy business report, legal document, etc. Effectively utilizing ChatGPT's summarizing ability, it can extract key information from a long article and generate a summary, helping us compress while not missing key information, improving reading efficiency. The method for generating summary prompts is simple. You can upload a document or give it a string of long text, and then ask: **Please generate a summary for this article.** This chapter is relatively simple, and I won't expand further.

### Chapter 5: Inferring

This chapter mainly introduces AI's reasoning ability. Reasoning is a very interesting capability of AI. When you give it a question or a topic, it will try to generate a reasonable and helpful answer based on the knowledge and skills it has already learned. It is implemented based on Zero-Shot Learning. A colloquial explanation is:

> The model uses existing knowledge or information to handle new, unknown situations. When reasoning, the model may need to predict unknown results based on known facts or rules.

You can understand this through an example:

For instance, if you tell ChatGPT, "It's raining today, I didn't bring an umbrella, will I get wet?"

ChatGPT will combine its "learned" knowledge about rain, umbrellas, and wetness, and give an answer like "Yes, if you walk in the rain without an umbrella, you may get wet."

This involves a simple reasoning: rain get people wet, an umbrella can prevent people from getting wet, a person without an umbrella will get wet in the rain.

### Chapter 6: Transforming

Transforming might be one of AI's best skills. The academic description of Transforming is:

> Transforming ability mainly refers to its ability to convert one form of information into another, or to convert information from one context, tone, or style to another.

This might be a bit abstract, here are some common application scenarios:

1. **From unstructured information to structured information**: Key information can be extracted from unstructured text data and converted into structured formats, such as JSON, XML, etc. This is useful when processing a large amount of unstructured data.
2. **From one language to another**: Although AI is not a professional translation tool, the translation capability it currently demonstrates really crushes all translation software on the market. Here I recommend an AI-based conversion tool I'm currently using: **OpenAI Translator**. It's open-source software you can find on GitHub.
3. **From one tone or style to another**: A text can be converted from one tone or style to another. For example, it can convert a formal business report into a more colloquial, easy-to-understand language.
4. **Convert complex concepts or information into an easy-to-understand form**: For example, it can convert a scientific report on climate change into a story suitable for children, or convert a set of complex data into simple charts or infographics.
5. **From text to audio or video scripts**: A piece of text can be converted into a script suitable for recording as audio or video.

These are just some possible application scenarios. AI's conversion capability can play a role in many other scenarios, depending on specific needs and environments.

### Chapter 7: Expanding

Expanding capability mainly refers to its ability to generate more content or information from given initial information or prompts. Simply put, it's the opposite of Summarizing; it generates long text based on short text. For example, articles, stories, conversations, etc. Here are some possible application scenarios:

1. **Writing assistance**: If you're stuck while writing, you can give it a short prompt and let it generate more content.
2. **Report generation**: If you need to write an article or report on a specific topic, you can give it a short overview or outline and let it generate the full article or report.
3. **Novel writing**: If you want to create a new story, you can give it a short plot summary and let it generate a complete story.
4. **Education and learning**: In education and learning scenarios, it can be used to generate teaching materials, such as explanations, case studies, questions and answers, etc.

Example:

Suppose we give AI a prompt like this:

```
Please generate a story based on the following prompt: On a beautiful morning, Jack woke up and found his pet parrot missing.
```

It will generate a story like this:

```
On a beautiful morning, Jack woke up and found his pet parrot missing. His eyes was immediately drawn to the empty corner of the cage, the door half open, the parrot's food untouched, everything appeared exceptionally quiet, in sharp contrast to the past laughter and joy.

He was extremely anxious and hurriedly searched the house; however, he did not find any trace of the parrot in the house. His heart sank, he thought maybe the parrot just flew out to play for a while and would be back soon. However, the whole morning passed, and the parrot still hadn't returned.

The afternoon sun shone on the garden, and Jack decided to search the garden and the nearby forest for the parrot. He called the parrot's name, but only the sound of the breeze blowing through the leaves replied. Jack became increasingly uneasy; he knew it was impossible for the parrot to have gone too far.

Just then, he saw a parrot feather, with some familiar claw marks next to it. His heart raced, and he followed these clues deep into the forest. In the depths of the forest, he saw his parrot, standing on a tall oak tree, next to a nest of newly hatched little birds.

It turned out that the parrot followed a mother bird here to help it take care of the newly hatched birds. Seeing this scene, Jack smiled; he knew his parrot was a kind creature, and its disappearance was to do a good deed.

That day, Jack and his parrot spent a beautiful day together in the forest. They helped the little birds find food and played together in the woods. In the evening, the parrot returned to the cage, and Jack knew that no matter where the parrot flew, it would return to him, because this was its home.
```

In this example, ChatGPT expanded a complete story from a simple prompt, including character actions, feelings, and the development and conclusion of the story.

### Conclusion

Andrew Ng's Prompt Engineering course mainly explains the basic principles of using Prompts and how LLM models are used in various scenarios.

Remember the following principles when using Prompts:

1. Clear and specific instructions.
2. Sufficient context and enough conversation.
3. Ask to show information sources to avoid AI fabricating facts.
4. Use structured output methods, such as JSON, XML, HTML, etc., as these are outputs AI is good at.
5. Reasonable expectations; AI is not omnipotent.

These are all the contents of the course. The course content is not long; if you are interested, you can go to the official website to learn.
