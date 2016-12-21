#!/bin/sh

PI_IP=<example_ip>

echo "SFTPing into Pi now..."
sftp $PI_IP

put -r GoPiGoLocal

bye
echo "Files transferred succesfully!"
