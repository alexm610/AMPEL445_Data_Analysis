#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "mat.h"
#include "engine.h"
#include "mex.h"

#define  BUFSIZE 256

int main(int argc, char **argv)
{
	Engine *ep;
	mxArray *T = NULL, *result = NULL;
	char buffer[BUFSIZE+1], str1[50], str2[5];
	double time[10] = { 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0 };
	MATFile *pmat;
    const char **dir;
    const char *name, *file, *input_file;
    int	  ndir;
    int	  i;
    mxArray *pa, *power, *wavelength, *fibre1, *fibre2, *fibre3;
	file = argv[1];
		/*
	 * Call engOpen with a NULL string. This starts a MATLAB process 
     * on the current host using the command "matlab".
	 */
	if (!(ep = engOpen(""))) {
		fprintf(stderr, "\nCan't start MATLAB engine\n");
		return EXIT_FAILURE;
	}

    /*
    * Open file to get directory
    *//*
	printf("Reading file %s...\n\n", file);
    pmat = matOpen(file, "r");
    if (pmat == NULL) {
      printf("Error opening file %s\n", file);
      return(1);
    }
  
    /*
    * get directory of MAT-file
    *//*
    dir = (const char **)matGetDir(pmat, &ndir);
    if (dir == NULL) {
      printf("Error reading directory of file %s\n", file);
      return(1);
    } else {
      printf("Directory of %s:\n", file);
      for (i=0; i < ndir; i++)
        printf("%s\n",dir[i]);
    }
    mxFree(dir);

	// get scandata variable from .MAT file
	fibre1 = matGetVariable(pmat, "scandata");
	if (fibre1 == NULL) {
		printf("ERROR reading scandata");
		return(1);
	}
	printf("number of dimensions: %d\n\n", mxGetNumberOfDimensions(fibre1));

*/
	
	
	// file = load("argv[1]")
	input_file = malloc(strlen(argv[1]) + 15);
	strcpy(buffer, "file = load(\"");
	strcat(buffer, argv[1]);
	strcat(buffer, "\")");
	printf("\n\t %s\n\n", buffer);
	// MATLAB commands to load data 
	engEvalString(ep, buffer); // file = load("argv[1]")
	engEvalString(ep, "data = file.scandata");
	engEvalString(ep, "fibre1 = data.power(:,1)");
	engEvalString(ep, "fibre3 = data.power(:,2)");
	engEvalString(ep, "fibre4 = data.power(:,3)");
	engEvalString(ep, "wavelength = data.wavelength(1,:)");
	wavelength = mexGetVariable("global", "wavelength");

	buffer[BUFSIZE] = '\0'; // terminate output buffer with NULL character
	engOutputBuffer(ep, buffer, BUFSIZE); // have all MATLAB outputs returned to buffer[]; so we can print to screen 
	while (result == NULL) {
	    char str[BUFSIZE+1];
	    char *input = NULL;
	    /*
	     * Get a string input from the user
	     */
	    printf("Enter a MATLAB command to evaluate.  This command should\n");
	    printf("create a variable X.  This program will then determine\n");
	    printf("what kind of variable you created.\n");
	    printf("For example: X = 1:5\n");
	    printf(">> ");

	    input = fgets(str, BUFSIZE, stdin);

	    /*
	     * Evaluate input with engEvalString
	     */
	    engEvalString(ep, str);
	    
	    /*
	     * Echo the output from the command.  
	     */
	    printf("%s", buffer);
	    
	    /*
	     * Get result of computation
	     */
	    printf("\nRetrieving X...\n");
	    if ((result = engGetVariable(ep,"X")) == NULL)
	      printf("Oops! You didn't create a variable X.\n\n");
	    else {
		printf("X is class %s\t\n", mxGetClassName(result));
	    }
	}

	/*
	 * We're done! Free memory, close MATLAB engine and exit.
	 */
	printf("Done!\n");
	mxDestroyArray(result);
	engClose(ep);
	matClose(pmat);
	return EXIT_SUCCESS;
}