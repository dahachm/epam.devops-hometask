f = open("dumpfile", "rb")
f.seek(24,0)
while True:
        buf = f.read(30)
        if len(buf)<30:
                break
        buf  = f.read(2)
        size = f.read(2)
        buf  = f.read(8)

        src   = f.read(4)
        dst   = f.read(4)
        type  = f.read(1)
        code  = f.read(1)
        chsum = f.read(2)
        
        size = '{}{}'.format(*bytearray(size))
        size_to_read = int(size) - 20 - 4
        #data = f.read(size_to_read)

        print("src: " + '{}.{}.{}.{}'.format(*bytearray(src)) + " > dst: " + '{}.{}.{}.{}'.format(*bytearray(dst)))

	type = int('{}'.format(*bytearray(type)))
        code = int('{}'.format(*bytearray(code)))

	print ("ICMP type = " + str(type) + " code = " + str(code) + ": ")        

        if type == 0:
            print ("\tEcho relpy.")
            id  = f.read(2)
            seq = f.read(2)
            size_to_read -= 4
            id  = str(int('{}{}'.format(*bytearray(id))))
            seq = str(int('{}{}'.format(*bytearray(seq))))
            print ("id = " + id + ", seq = " + seq)

        if type == 3:
            print ("\tDestination Unreachable.")
            if code == 0:
                print ("\t\tDestination network unreachable.")
            if code == 1:
                print ("\t\tDestination host unreachable.")
            if code == 2:
                print ("\t\tDestination protocol unreachable.")
            if code == 3:
                print ("\t\tDestination port unreachable.")
            if code == 4:
                print ("\t\tFragmentation required, and DF flag set.")
            if code == 5:
                print ("\t\tSource route failed.")
            if code == 6:
                print ("\t\tDestination network unknown.")
            if code == 7:
                print ("\t\tDestination host unknown.")
            if code == 8:
                print ("\t\tSource host isolated.")
            if code == 9:
                print ("\t\tNetwork administratively prohibited.")
            if code == 10:
                print ("\t\tHost administratively prohibited.")
            if code == 11:
                print ("\t\tNetwork unreachable for ToS.")
            if code == 12:
                print ("\t\tHost unreachable for ToS.")
            if code == 13:
                print ("\t\tCommunication administratively prohibited.")
            if code == 14:
                print ("\t\tHost Precedence Violation.")
            if code == 15:
                print ("\t\tPrecedence cutoff in effect.")

        if type == 5:
            print ("\tRedirect Message: ")
            if code == 0:
                print ("\t\tRedirect Datagram for the Network.")
            if code == 1:
                print ("\t\tRedirect Datagram for the Host.")
            if code == 2:
                print ("\t\tRedirect Datagram for the ToS & network.")
            if code == 3:
                print ("\t\tRedirect Datagram for the ToS & host.")            

        if type == 8:
            print ("\tEcho Request.")
            id  = f.read(2)
            seq = f.read(2)
            size_to_read -= 4
            id  = str(int('{}{}'.format(*bytearray(id))))
            seq = str(int('{}{}'.format(*bytearray(seq))))
            print ("id = " + id + ", seq = " + seq)

        if type == 9:
            print ("\tEcho Advertisment.")

        if type == 10:
            print ("\tRouter Solication: Router discovery/selection/solicitation.")

        if type == 11:
            print ("\tTime Exceeded: ")
            if code == 0:
                print ("\t\tTTL expired in transit.")
            if code == 1:
                print ("\t\tFragment reassembly time exceeded.")   

        if type == 12:
            print ("\tParameter Problem: Bad IP header: ")
            if code == 0:
                print ("\t\tPointer indicates the error.")
            if code == 1:
                print ("\t\tMissing a required option.")
            if code == 2:
                print ("\t\tBad length.")        

        if type == 13:
            print ("\tTimestamp.")
            id  = f.read(2)
            seq = f.read(2)
            size_to_read -= 4
            id  = str(int('{}{}'.format(*bytearray(id))))
            seq = str(int('{}{}'.format(*bytearray(seq)))) 
            print ("id = " + id + ", seq = " + seq)

        if type == 14:
            print ("\tTimestamp reply.")
            id  = f.read(2)
            seq = f.read(2)
            size_to_read -= 4
            id  = str(int('{}{}'.format(*bytearray(id))))
            seq = str(int('{}{}'.format(*bytearray(seq))))
            print ("id = " + id  + ", seq = " + seq)

        if type == 40:
            print ("\tPhoturis, Security failures.")

        data = f.read(size_to_read)        
        print ("DATA (" + str(size_to_read) + " bytes): " + "".join("%02x " % b for b in bytearray(data)))
	print

f.close()
