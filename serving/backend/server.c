#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <pthread.h>

#define BUFFER_SIZE 1024

char ip[5][16] = {"192.168.0.1", "192.168.0.2", "192.168.0.3"};
int num_model_serv = 3;

void* handle_request(void* arg)
{
    char buffer[BUFFER_SIZE * BUFFER_SIZE];
    int bytes_read, bytes_written, clnt_sock, model_serv_sock;
    struct sockaddr_in model_serv_addr;

    clnt_sock = *(int*)arg;
    
    bytes_read = 0;
    while(1)
    {
        bytes_read = bytes_read + read(clnt_sock, &(buffer[bytes_read]), sizeof(buffer)-1-bytes_read);
        if(buffer[bytes_read-1]=='}')
        {
            break;
        }
    }
    buffer[bytes_read] = 0;

    model_serv_sock=socket(PF_INET, SOCK_STREAM, 0);
	if(model_serv_sock == -1)
    {
        exit(-1);
    }
    memset(&model_serv_addr, 0, sizeof(model_serv_addr));
	model_serv_addr.sin_family=AF_INET;
	model_serv_addr.sin_addr.s_addr=inet_addr(ip[clnt_sock % num_model_serv]);
	model_serv_addr.sin_port=htons(30009);

    if(connect(model_serv_sock, (struct sockaddr*)&model_serv_addr, sizeof(model_serv_addr))==-1)
    {
        exit(-1);
    }
    
    buffer[118] = '0';
    buffer[119] = '9';
    
    write(model_serv_sock, buffer, bytes_read);
    
    bytes_read = 0;
    while(1)
    {
        bytes_read = bytes_read + read(model_serv_sock, &(buffer[bytes_read]), sizeof(buffer)-1-bytes_read);
        if(buffer[bytes_read-1]=='}')
        {
            break;
        }
    }
    buffer[bytes_read] = 0;
    printf("%s\n", buffer);
    
    write(clnt_sock, buffer, bytes_read);

    close(model_serv_sock);
    close(clnt_sock);
}

int main(int argc, char *argv[])
{
	int serv_sock, clnt_sock;
    int* ptr;
    struct sockaddr_in serv_addr, clnt_addr;
	socklen_t clnt_addr_size;
    pthread_t t_id;
	
	if(argc!=2)
    {
		printf("Usage : %s <port>\n", argv[0]);
		exit(1);
	}
	
	serv_sock=socket(PF_INET, SOCK_STREAM, 0);
	if(serv_sock == -1)
    {
        exit(-1);
    }
	
	memset(&serv_addr, 0, sizeof(serv_addr));
	serv_addr.sin_family=AF_INET;
	serv_addr.sin_addr.s_addr=htonl(INADDR_ANY);
	serv_addr.sin_port=htons(atoi(argv[1]));
	
	if(bind(serv_sock, (struct sockaddr*) &serv_addr, sizeof(serv_addr))==-1)
    {
        exit(-1);
    }
	
	if(listen(serv_sock, 5)==-1)
    {
        exit(-1);
    }

    clnt_addr_size=sizeof(clnt_addr);
    while(1)
    {  
    	clnt_sock=accept(serv_sock, (struct sockaddr*)&clnt_addr,&clnt_addr_size);
    	if(clnt_sock==-1)
        {
            exit(-1);
        }
        ptr = (int*)malloc(sizeof(int));
        *ptr = clnt_sock;
        if(pthread_create(&t_id, NULL, handle_request, (void*)ptr)!=0)
        {
            exit(-1);
        }
    }
    
	close(serv_sock);
    
	return 0;
}