Imagine you want to organize your team’s feature backlog. Projects, GitHub's built in program management tool, is a perfect way to organize and prioritize your team’s work in a single space. 

In this unit you’ll learn:
- The difference between Projects vs Projects (Classic)
- How to create a Project
- How to set the name, description, and README of your Project
- How to add issues and pull requests to your Project

## Projects vs Projects (Classic)
Before we dive into Projects, let's first go over how Projects has improved by comparing Projects to Projects (Classic).

|  | Projects | Projects (Classic) | 
|--------|--------|--------| 
| Tables and Boards | Boards, Lists, Timeline Layout | Boards | 
| Data | Sort, rank, and group items by custom fields such as text, number, date, iteration and single select | Columns and Cards | 
| Insight |  Rewrite what should go here | Rewrite what should go here | 
| Automation | Research what should go here | Research what should go here | 

The new GitHub Projects provides a richer experience that allows you to keep track of your work, where you work. Let's dive a bit deeper into the changes that have been made.

### Tables and boards:
- Plan and track work in a table or board view
- Rank, sort, and group within a table by any custom field
- Create draft issues with detailed descriptions and metadata
- Materialize any perspective with tokenized filtering and saved views
- Customize cards and group-by in project boards
- Real-time project updates and user presence indicators

### Data:
- Define custom fields of type: text, number, date, iteration, and single select
- Configure iterations with flexible date ranges and breaks to represent your sprints, cycles, or quarterly roadmap
- View linked pull requests and reviewers in both table and board views

### Insight:
- Create and configure custom bar, column, line, and stacked area charts
- Use aggregation functions like sum, count, average, min, and max to get the proper insight
- Persist charts and share them with a URL to keep everyone in the know

### Automation
- GraphQL ProjectsV2 API
- GitHub app project scopes
- Webhooks events for project item metadata updates
- GitHub Action to automate adding issues to projects

## Creating an organization level Project

First we want to lay the foundation of your Project by creating a new Project. This is fairly simple and you can do this relatively quickly.

1. First, in the top right corner of GitHub.com, click your profile photo, then click **Your organizations**.

:::image type="content" source="../media/your-organizations.png" alt-text="Profile Dropdown Menu that includes Your profile, Your repositories, Your codespaces, Your organizations and Your enterprises- with Your Organization option highlighted.":::

2. Once on **Your organization page**, click the name of your organization you want to create a new Project for.
3. Under your organization name, click **Projects**.
4. Then click the green button labeled **New Project**. 
5. Next it will ask you to select either a template or an empty project. Let’s start from scratch and select **Table** and then click the green **Create** button. 

You just created a Project! 

You can also create a personal Project by clicking your profile photo and navigating to **Your projects**. Once you are on your Projects page, you can simply click on the green button titled **New project**. 

## Setting your project’s name, description, and README

Let’s define your Project in a couple of different ways so that your team can easily understand what you're tracking. 

1. To edit your Project’s name, description and README navigate to your newly created project and in the top right, click the 3 dots to open the menu.
1. In the menu, click **Settings**.
1. And here you can edit the name of the Project and it will save automatically.
1. Next add a short 5-7 word description of the Project and make sure to click **Save** afterwards. 
1. Then to update your Project’s README, under **README**, type out a bit more information for your team to understand why you created this Project and what you hope to accomplish with it. And when you’re done make sure to click **Save**. 

:::image type="content" source="../media/edit-readme.png" alt-text="An Example of a Project README that is highlighted with example texts that describes the users Project.":::


## Adding issues and pull requests to your Project

Adding in issues and pull requests to your Project is what makes it so powerful. It allows you to know the status of tasks your team is working on in order to coordinate and complete your goals. 

Let’s go through the different ways to add issues and pull requests to your Project. 

### Adding an existing issue and pull request
1. First, copy the url of an existing issue or pull request. 
2. Next, place your cursor in the bottom row of the Project, next to the **+** and paste the URL of your issue or pull request. 

:::image type="content" source="../media/paste-url-to-add.png" alt-text="An Image of a Project in List view with an example of a URL of an Issue being pasted into the Projects.":::

3. Finally press return and your issue or pull request will appear as a task in your Project.

### Searching for an existing issue and pull request
1. You can also search for existing issues or pull request by simply adding a new item. 
2. Enter #.

:::image type="content" source="../media/add-item-select-repo.png" alt-text="Example of a Project in List view, focused on searching for an existing Issue or Pull Request by adding a # and typing in key phrase.":::

3. Select the repository where the pull request or issue is located. You can type part of the repository name to narrow down your options.
4. Select the issue or pull request. You can also start typing the title to find the one you want. 

### Bulk adding issues and pull request

If you have an existing repository that you’d like to track using Projects bulk adding issues and pull requests saves you time and allows you to start organizing your team faster. 

1. First, in the bottom row of the project, click **+**. 
2. Next, click **Add item from repository**. 
3. To change the repository, click the dropdown and select a repository. The issues and pull requests will populate.
4. You can either select all or select the ones you want to include.

:::image type="content" source="../media/add-bulk-select-repo.png" alt-text="Example of Bulk Adding Issues and Pull requests from a Repository, with the option to search for specific Issues or Pull Requests highlighted.":::

5. Once you are ready to add the issues and pull requests to your project, click on green button titled **Add selected item** in the bottom right corner. 

In the next unit you'll learn how to organize and prioritize your project in order to keep your tasks on track.
