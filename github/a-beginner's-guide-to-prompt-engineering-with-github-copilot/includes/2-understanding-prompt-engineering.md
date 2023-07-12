:::image type="content" source="../media/prompt-engineering-header.png" alt-text="REPLACE-ME":::

GitHub Copilot and other Generative AI coding tools are transforming the way developers approach daily coding tasks. From documenting your codebases to generating unit tests, these tools are helping to accelerate your workflows. However, just like with any emerging tech, there’s always a learning curve. As a result, it can sometimes feel frustrating when AI-powered coding assistants don’t generate the output you want. (Feel familiar?)

It's not uncommon to feel frustrated when you don't receive the expected results, and then see examples of other developers being successful using these same tools. For example, someone using GitHub Copilot for the first time may ask it to solve a problem or provide a solution to a specific coding question only to get back an incongruent suggestion or no suggestion at all. This can be discouraging and can result in many hours tinkering with the tool and then feeling lucky if you got what you're looking for. But, as it turns out, these discouraging situations are most likely a result of using the tool wrong. In fact, there is a concept called prompt engineering that we'll explore in this module, and by using best practices, you'll be able to more accurately get the results and code suggestions you're looking for.

But, before we dive into these best practices, let's start with the basics of GitHub Copilot and prompt engineering.

## What is GitHub Copilot?

GitHub Copilot is an AI pair programmer developed by GitHub. It's powered by the OpenAI Codex, a generative pre-trained language model created by OpenAI and provides contextualized code suggestions based on context from comments and code. To use it, you can install the GitHub Copilot extension available to you in the following Integrated Development Environments (IDEs):

- Visual Studio
- Visual Studio Code
- Neovim
- JetBrains IDEs (IntelliJ, PyCharm, WebStorm, etc)

Under the hood, GitHub Copilot draws context from comments and code, instantly suggesting individual lines and whole functions.

## What is prompt engineering?

Prompt engineering is the practice of giving an AI model specific instructions to produce the results you want. A prompt is a sequence of text or a line of code that can trigger a response from an AI model. These AI models will only do what you tell them to do, so the more specific the instructions the better the results will be. Being vague or simple in your instructions will often provide a wide variety of undesired results.

Then same concept is true in everyday situations. For example, if you asked someone to make you a sandwich and the only instructions you gave them was, "Make me a sandwich", then it's very likely you'll get a sandwich that you didn't want. However, if instead you gave them a series of specific steps or instructions, you can get closer to your desired outcome. So, If I wanted a turkey, bacon, and avocado sandwich, I could get closer to my desired outcome with the following prompt.

- Open the bag of wheat bread and take two slices of the bread out of the bag
- Lay the slices of bread side by side on the table
- Place two slices of turkey on one slice of bread
- On the same slice of bread, place two pieces of cooked bacon
- And so on...

Without these detailed instructions, the desired outcome can be disappointing and frustrating. Similarly, GitHub Copilot needs clear, step-by-step instructions to generate the code that best helps you and provide you with your desired outcome.

For a more code specific example, let's see what this would look like using p5.js, which is a JavaScript library for creative coding and is a fun way to create images with code. 

### Example of a basic prompt

Let's use GitHub Copilot to create an image of a boat using the below prompt.

`
// draw a brown wooden boat on top of a blue ocean with a sun.
`

GitHub Copilot returns with the following code for the image. It's somewhat relevant but it's hard to tell if that is a boat. We can do better.

:::image type="content" source="../media/simple-prompt.png" alt-text="REPLACE-ME":::

Basics prompts such as this often return irrelevant suggestions—or sometimes no suggestions at all. As you learn how GitHub Copilot processes information, you can adjust the way you communicate with it and adjust your prompt to generate more accurate results. Let's try this again, but with a better prompt.

### Example of a detailed prompt

When prompting GitHub Copilot, think of the process as having a conversation with someone: How should I break down the problem so we can solve it together? How would I approach pair programming with this person?

Let's expand on the above basic prompt and provide GitHub Copilot a big picture description of what we want it to generate by using the prompt below.

```
/* draw a brown wooden boat with a white sail on top of a blue ocean.
- The sky is light blue with one white cloud.
- The cloud has three different sized circles that overlap each other.
- The sun is a yellow circle inside a yellow-orange circle inside an orange circle in the top right corner.
- The sail is a large white triangle connected to the top of the dark brown mast down to the tip of the front of the boat.
- The boat is curved at the bottom and has a dark brown rectangle for the body.
*/
```

As you can see, GitHub Copilot was able to more accurately provide a result that we were looking for.

:::image type="content" source="../media/detailed-prompt.png" alt-text="REPLACE-ME":::

When you provide specific details, GitHub Copilot will be able to generate more accurate code suggestions. For example, if you want GitHub Copilot to retrieve data from an API, you need to tell it what type of data you want to retrieve, how to process the data, and what API endpoint you're hoping to hit.

## 6 best practices for prompt crafting with GitHub Copilot

We've seen the impact that detailed prompts can have with our desired outcome, but let's take this further and look at 6 best practices for crafting prompts using GitHub Copilot.

### 1. Set the stage with a high-level goal

This is most helpful if you have a blank file or empty codebase. In other words, if GitHub Copilot has zero context of what you want to build or accomplish, setting the stage for the AI pair programmer can be really useful. It helps to prime GitHub Copilot with a big picture description of what you want it to generate—before you jump in with the details.

When prompting GitHub Copilot, think of the process as having a conversation with someone: How should I break down the problem so we can solve it together? How would I approach pair programming with this person?

### 2. Make your ask simple and specific

Once you communicate your main goal to the AI pair programmer, articulate the logic and steps it needs to follow for achieving that goal. GitHub Copilot better understands your goal when you break things down. (Going back to the sandwich example, break the process down into discrete steps, don't write a paragraph describing the sandwich you want to make.)

In addition, let GitHub Copilot generate the code after each step, rather than asking it to generate a bunch of code all at once.

### 3. Give GitHub Copilot an example or two

Learning from examples is not only useful for humans, but also for your AI pair programmer. In addition to telling GitHub Copilot what you want it to do, you can also show it what you want it to do with examples in your preferred coding style. While GitHub Copilot is using an AI model that is already trained on a large amount of data, providing examples to GitHub Copilot help it understand the context and constraints of a particular code snippet. Showing AI models examples of what you want them to do is a common practice in machine learning.

### 4. Experiment and iterate with your prompts

If your initial prompt provides an unrelevant solution, delete the generated code suggestion, edit your comment with more details and examples, and try again! It's a learning process for you and GitHub Copilot. The more you use it, the better you'll get at communicating with GitHub Copilot. Just how conversation is more of an art than a science, so is prompt crafting. So, if you don’t receive what you want on the first try, recraft your prompt by following these best practices.

### 5. Keep a tab opened of relevant files in your IDE

GitHub doesn't have an exact number of tabs that you should keep open to help GitHub Copilot contextualize your code, but from users experience, it's reported that one or two is helpful.

GitHub Copilot uses a technique called neighboring tabs that allows the AI pair programmer to contextualize your code by processing all of the files open in your IDE instead of just the single file you’re working on. However, it’s not guaranteed that GitHub Copilot will deem all open files as necessary context for your code.

### 6. Use good coding practices

While GitHub Copilot can be a powerful tool for generating code suggestions, it's important to remember that it's not a replacement for your own programming skills and expertise. AI models are only as good as the data they have been trained on, Therefore, it's important to use these tools as aids and not rely on them entirely. It's important for you to still perform the following tasks when using GitHub Copilot:

- Review the code suggestions
- Run unit tests
- Manually test the code suggestions to ensure they work as intended
- Continue to use good coding practices. GitHub Copilot will adapt to follow your coding style and patterns as a guide when providing suggestions