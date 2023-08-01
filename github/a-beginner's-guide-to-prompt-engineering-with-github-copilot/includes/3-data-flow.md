:::image type="content" source="../media/data-flow.png" alt-text="REPLACE-ME":::

Now that we've covered the basics of prompt engineering, let's take a closer look at how GitHub Copilot works under the hood and better understand the inbound and outbound data flow that occurs when you initiate a prompt.

Using the above image for reference, GitHub Copilot's data flow can be dissected into the following steps;

- 1. Prompt is sent from the text editor to a proxy service
- 2. Synthesize solutions using the OpenAI Model
- 3. sdsdsd

## Step 1: Prompts are sent from the text editor to a proxy service

Because GitHub Copilot is based on the use of a plugin within your text editor, GitHub Copilot is scoped to your local environment within that text editor. It doesn't look at your Git repositories, your file systems, or any open browsers. However, if you have open files within your text editor, GitHub Copilot does look at those open files for context to better understand your code to provide you with more accurate suggestions.

When a prompt is sent from your text editor, GitHub Copilot will first look at the main open file and notice where your cursor is positioned within that file. Copilot will then pull a window of roughly 400 characters before and after your cursor, evaluate the code within that window, and then look at any open tabs within your text editor to see if there is anything useful it can reference to give a better prompt suggestion.

A common example of this is writing unit tests. If you're writing unit tests in one file, and the file you're testing is in an adjacent tab, GitHub Copilot will evaluate the initial code in the main file around your cursor, look at the code in that adjacent tab for additional context, and then use all of that information to provide you a better prompt suggestion.

### Encrypted data

It's important to note that all of this data is encrypted before it is sent over to the proxy service. The prompt is sent over HTTPS using TLS 1.2/1.3, the same secure method if you were to make a purchase with an online retailor. 

### Copilot Proxy Service

The proxy service is run in a GitHub owned Azure tenant. GitHub controls this proxy service and sets the specifications on how it runs the pre and post processing of the code that goes through the proxy service through a prompt. On the pre-processing side, once the prompt has been encrypted and it's been received by the proxy, the proxy service will decrypt the data, keep it in ram for processing, and filter the data for sensitive and inappropriate information while also running Microsoft's responsible AI toxicity filter. Here are a key items that will be filtered out through the proxy service that will be stripped out or ignored;

- Personally identifiable information (PII)
  - IP addresses, email addresses specific GitHub URLs
- Toxicity data
  - Hate speech, inappropriate words, abusive use of prompts, etc.

In addition to the filtering that takes place, the proxy service also runs a code classifier based on the prompt data. For example, is it code that the user wants back? If it is, what kind? Are the files in Java, Python, or something else? All of this information is what the proxy service is doing on the front end. Once this pre-processing is done, it remains in ram and nothing is ever stored at rest. It then gets re-encrypted and sent to the model.

## Step 2: Synthesize solutions using the OpenAI Model

