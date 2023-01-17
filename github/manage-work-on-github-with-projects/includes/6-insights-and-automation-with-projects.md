Now let's talk about how Projects can provide you with insights and how to make life a bit easier with automation.

## Insights with Projects

In this section we'll talk you through: 

- What are insights and how can they be useful
- Current charts and  historical charts
- Creating and customizing charts

### What are insights and how can they be useful

Insights with Projects allows you to view, create and customize charts that use items added to your Project as source data. When you create a chart, you set the filters, chart type, the information displayed, and the chart is available to anyone that can view the Project. You can generate two types of charts: current charts and historical charts.

### Current and Historical charts

As mentioned above there are two types of charts you can create from insights: current and historical charts. Below we dive into the differences between the two.

#### Current charts:

You can create current charts to visualize your Project items. For example, you can create charts to show how many items are assigned to each individual, or how many issues are assigned to each upcoming iteration.
You can also use filters to manipulate the data used to build your chart. For example, you can create a chart showing how much upcoming work you have, but limit those results to particular labels or assignees. 
:::image type="content" source="../media/column-chart-example.png" alt-text="Example of a current bar chart tracking the amount of hours spent per 7 iteration phases and color coded by amount of time spent on Bugs, Feedback, Backend, and UI work.":::

#### Historical charts:

Historical charts are currently available as a feature preview for organizations using GitHub Team and are generally available for organizations using GitHub Enterprise Cloud.
Historical charts are time-based charts that allow you to view your Project's trends and progress. You can view the number of items, grouped by status and other fields, over time.
The default "Burn up" chart shows item status over time, allowing you to visualize progress and spot patterns over time.
:::image type="content" source="../media/burnup-example.png" alt-text="Example of a historic stacked area line graph showing the amount of hours spent on to dos, in progress, and completed tasks during the month of July.":::

### Creating and customizing charts

Creating charts is simple, below are the steps to follow for when you want to create a new chart. 

1. Navigate to your Project.
2. In the top-right, to access insights, click the line graph button, when you hover above it, it'll be labeled as Insights 
3. In the menu on the left, click **New chart**.
4. Above the chart, type filters to change the data used to build the chart.
5. To the right of the filter text box, click **Save changes**.

Now that you’ve created a new chart, let’s customize it to fit your needs. 

1. First, navigate to your Project.
2. In the top-right, to access insights, click the line graph button, labeled Insights.
3. In the menu on the left, click on the chart you would like to configure.
4. On the right side of the page, click Configure. A panel will open on the right.
5. To change the type of chart, select the Layout dropdown and click on the chart type you want to use.
6. To change the field used for your chart's X-axis, select the X-axis dropdown and click the field you want to use.
7. Optionally, to group the items on your X-axis by another field, select Group by and click on the field you want to use, or click "None" to disable grouping.

## Automation with Projects

Work doesn’t have to take up too much work, especially when you use Projects. Let GitHub do some of the work for you by automating your Project.

There are two different ways you can automate your Project: 
- Built-in automation
- GraphQL API
- GitHub Actions

The easiest way to automate your Project would be to use Project’s built-in automation, while GraphQL and Actions you have more control over customizing automation. 
In the following sections we’ll walk you through how to utilize Project’s built-in automation and briefly go over GraphQL API and GitHub Actions automation. 

Let’s start with Project’s built-in automation. 

### How to configure built-in automation

With built-in automation, your Project will take newly created issues or pull requests and automatically put them into your Project with a Todo status, helping you stay aware of all of your work.

To enable automation first go to the top-right corner of your Project and click on the three dots to open the menu. 
1. Next, in the menu, click **Workflows**.
:::image type="content" source="../media/workflows-menu-item.png" alt-text="Workflows Menu on Projects that contains the options, Workflows, Archived items, and Settings with Workflows highlighted.":::
2. In the left column, under Default workflows, select **Item added to project**. 
:::image type="content" source="../media/default-workflows.png" alt-text="An Image of the menu to enable workflows once an action occurs. Options include Item added to project, Item reopened, Item closed, Code changes requested, Code review approved, Pull request merged with Item added to project highlighted":::
3. Now in the center of the page, where it says **When**, ensure that both issues and pull requests are selected.
4. Below click on **Set** and click **Status:Todo**.
5. Finally in the right corner of the page, ensure the toggle is turned **On**. 

Congratulations! You’ve just automated your project!

### GraphQL API 

If you are using GraphQL in GitHub, you can also utilize it to help automate your Project. For more information on using GraphQL API, see [Using the GraphQL API to automate your projects.](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/using-the-api-to-manage-projects) 

### GitHub Actions

GitHub Actions allows you the most customization for your Project’s automation. Learn more about automating workflows for your Project here, [Automating Projects using Actions.](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/automating-projects-using-actions)