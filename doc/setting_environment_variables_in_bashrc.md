# Setting environment variables in the .bashrc file.

> This page was created with the help of OpenAI ChatGPT

Setting environment variables in the .bashrc file allows you to define variables that are accessible to the shell and its subprocesses. This can be useful for storing information such as the location of your project directories, the default editor you want to use, or the default version of a programming language you want to use.

To set an environment variable in the .bashrc file, you can use the export keyword followed by the name of the variable and its value. For example, to set a variable called PROJECT_HOME that holds the path to your project directories, you could add the following line to your .bashrc file:

```bash
export PROJECT_HOME="/path/to/my/project/dir"
```

Once you have set an environment variable in your .bashrc file, you can access its value in your shell by referencing its name using the $ character. For example, you could use the cd command to change to your project directory by using the PROJECT_HOME variable like this:

```bash
cd $PROJECT_HOME
```

Keep in mind that changes to your .bashrc file will not take effect until you either log out and log back in, or you source the file using the source command:

```bash
source ~/.bashrc
```

Sourcing the .bashrc file allows you to apply the changes you have made to the file without having to log out and log back in. This can be useful if you want to test your changes without losing your current shell session.