#include <iostream>
#include <fcntl.h>
#include <unistd.h>
#include <termios.h>
using namespace std;

//Functions
int initSerial(const char* device)
{
    int fd = open(device, O_RDWR | O_NOCTTY | O_NDELAY);
    if(fd == -1)
    {
        perror("Open Port: Unable to open serial port");
        return -1;
    }

    struct termios options;
    tcgetattr(fd, &options);

    //Set baud-rate
    cfsetispeed(&options, B9600);
    cfsetospeed(&options, B9600);

    options.c_cflag &= ~PARENB;        //no parity
    options.c_cflag &= ~CSTOPB;        //1 stop bit
    options.c_cflag &= ~CSIZE;
    options.c_cflag |= CS8;            //8 data bits
    options.c_cflag &= ~CRTSCTS;       //no hardware flow control
    options.c_cflag |= CREAD | CLOCAL; //enable receiver, local mode

    tcsetattr(fd, TCSANOW, &options);

    return fd;
}

void sendCommand(int fd, char command)
{
    write(fd, &command, 1);   //one byte over serial
}

int main()
{
    const char* serialPort = "/dev/ttyUSB0";
    int fd = initSerial(serialPort);

    if(fd == -1)
    {
        return -1;   //serial port can't be opened
    }

    char command;
    cout << "Enter command (1 - turn on, 0 - turn off)" << endl;

    while(true)
    {
        cin >> command;

        if(command == '1' || command == '0')
        {
            sendCommand(fd, command);
        }
        else
        {
            cout << "Invalid entry" << endl;
        }
    }

    close(fd);
    return 0;
}

