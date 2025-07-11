async def handle_neofetch(message):
    neofetch_text = """\
                                              byakuren@server 
                             ....             --------------- 
              .',:clooo:  .:looooo:.          OS: Red Star OS x86_64 
           .;looooooooc  .oooooooooo'         Host: HP t420 Dual Core TC 
        .;looooool:,''.  :ooooooooooc         Kernel: 3.6.9-63-salakau 
       ;looool;.         'oooooooooo,         Uptime: 1 decade 
      ;clool'             .cooooooc.  ,,      Packages: 897 (pingas)
         ...                ......  .:oo,     Shell: discord 1.1.1
  .;clol:,.                        .loooo'    Terminal: /dev/pts/1 
 :ooooooooo,                        'ooool    CPU: AMD GX-217GA SOC (2) @ 1.6GHz 
'ooooooooooo.                        loooo.   GPU: ATI Radeon HD 8280E 
'ooooooooool                         coooo.   Memory: 0.60 GiB / 128 GiB (0%) 
 ,loooooooc.                        .loooo.   Network: 10 Gbps 
   .,;;;'.                          ;ooooc    BIOS: China Telecom 2.9 (05/04/2015) 
       ...                         ,ooool. 
    .cooooc.              ..',,'.  .cooo.                             
      ;ooooo:.           ;oooooooc.  :l.                              
       .coooooc,..      coooooooooo.       
         .:ooooooolc:. .ooooooooooo'       
           .':loooooo;  ,oooooooooc        
               ..';::c'  .;loooo:'         
                             .             
"""
    await message.channel.send(neofetch_text)