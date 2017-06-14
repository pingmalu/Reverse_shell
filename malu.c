/*
 提权
 Mail : malu#malu.me
*/
#include <stdio.h> 
#include <stdlib.h> 
#include <sys/types.h> 
#include <unistd.h> 
int main(int argc, void **argv){
	if(argc<2){
		return 0;
	}
        uid_t uid ,euid,i; 
        uid = 0;
        euid = geteuid();
        char execname[10240];
        if(setreuid(euid, uid)){   
                perror("setreuid"); 
        }else{
                sprintf(execname, "%s",argv[1]);
                for(i=2;i<argc;i++){
                	sprintf(execname, "%s %s",execname,argv[i]);
		}
                system(execname);
                return 0;  
        }
}
