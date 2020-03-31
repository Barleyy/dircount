# dircount

We are creating esoteric programming language (https://en.wikipedia.org/wiki/Esoteric_programming_language), which has it's syntax represented as hierarchical directory strucutre.
Based on how many directories are included in currently analized folder, specific action is taken.

For example:
Let's suppose that 2 directories means expression, then number of directories if first sub-directory determines which expression it is. Let it be declaring variable for 1 sub-directory. Then count of directories in mentioned first sub-directory holds information about type of to be declared variable. If it's 3, then we are going to declare integer. Now first sub-folder contains of 16 folder, each is checked if it's empty or not. Empty dir represents binary 0 and not empty one 1. Based on that int value is calculated.
Example of declaring int with value of 5:

![](/example.png)

In this project, we are going to create interpreter for this language. For this task we will use in python.
