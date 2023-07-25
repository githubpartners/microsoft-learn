:::image type="content" source="../media/data-flow.png" alt-text="REPLACE-ME":::

Now that we've covered the basics of prompt enginnering, let's take a closer look at how GitHub Copilot works under the hood and better understand the data flow that occurs when you initiate a prompt.

Using the above image for reference, GitHub Copilot's data flow can be dissected into the following steps;

- 1. Prompt is sent from the text editor to a proxy service
- 2. 
- 


## Step 1: Prompts are sent from the text editor to a proxy service

Because GitHub Copilot is based on the use of a plugin within your text editor, GitHub Copilot is scoped to your local environment within that text editor. It doesn't care about your Git repositories, your file systems, or open browsers you have. 