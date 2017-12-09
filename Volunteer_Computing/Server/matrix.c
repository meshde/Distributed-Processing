#include <stdio.h>
#include <stdlib.h>

int getInteger(char);
int getNumber(FILE *);
void getArray(FILE *,int *,int);
void printArray(int *,int);
int multiply(int *,int *,int);

int main(int argc,char *argv[]){
	int n;
	int arr[100];
	int b[100];
	char *file = argv[1];
	FILE *fptr;

	fptr = fopen(file,"r");
	
	fscanf(fptr,"%d",&n);
	getArray(fptr,arr,n);
	getArray(fptr,b,n);

	int ans = multiply(arr,b,n);

	printf("%d\n",ans);
	return 0;
}

void getArray(FILE *fptr, int *arr, int n){
	for(int i=0;i<n;i++){
		fscanf(fptr,"%d",&arr[i]);
	}
	return;
}

void printArray(int *arr,int n){
	for(int i=0;i<n;i++){
		printf("%d,",arr[i]);
	}
	printf("\n");

	return;
}

int multiply(int *a,int *b,int n){
	int i=0;
	int ans = 0;
	for(i=0;i<n;i++){
		ans += (a[i]*b[i]);
	}
	return ans;
}


int getInteger(char x){
	return (x - '0');
}

int getNumber(FILE *fptr){
	char ch = fgetc(fptr);
	int ans = 0;
	while(ch != ' ' || ch != '\n' || ch != '\r'){
		printf("%c\n",ch);
		ans = (ans * 10) + getInteger(ch);
		ch = fgetc(fptr);
	}
	return ans;
}

// void getArray(FILE *fptr, int **arr,int n){
// 	int i = 0;
// 	for(i=0;i<n;i++){
// 		*(*arr + i) = getNumber(fptr);
// 	}
// 	return;
// }