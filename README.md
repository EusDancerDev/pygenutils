* Originally created on Mon Apr 16 2024 and re-created on Mon Jun 10 2024
  due to critical failure in trying to reconcile local and remote work.
* This project is a continuation of the almost-the-same
  referenced *pytools.old* repo.
  
* The old project was in need of major improvements:
	- Modules visible from anywhere:

    	- As of the mentioned date, it wasnt' until I learned from the Advanced Course in Python
	      that there is another simpler and faster way to import custom modules.
    	- Until now, there was a program called 'setup_repo.py' which served as an initializator,
	      which, once the repository was cloned, it simulated am instalation for the first time,
    	  asking to the user if it wanted to :

			1. Conserve every content in the same directory the repo had been cloned
			   (default option).
			2. Move everything to an user-defined directory.
	
		- After choosing the directory, the initializator writes in the path /home/{user}
		  a very simple and short program where it creates a function, which returns the 
		  recently chosen diectory.
	
		- Because there are modules that depend on other modules, there was need of 
		  remembering and defining the paths of all these dependency modules, which 
		  was performed by a snippet defined in every single of them.

			- It takes advantage of precisely defining the /home path (Path.home())
			- The program is imported and its function is called, returning the path
			  where the repo has been cloned.
			- From now on the directories of the dependency modules are defined,
			  as well as method aliases, if the function calling syntax string was too long.

			- In order to track record of every defined path and make the definitions effective,
			  these paths are stored in a list of module paths, so that the interpreter searches 
			  in for the required modules (sys.path)

	- Huge level-up computation performance
	- Unification of case usages
	- Elimination of redundant conditional and instantiation instructions
	- Possible incorporation of OOP

* This project aims to perform and continue improving the mentioned steps.
