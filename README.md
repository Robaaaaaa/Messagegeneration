﻿# Crew-AI-Research-Tool
# Messagegeneration
try {               
>>   cmd /c "(python process_in_batches.py --batch-size 5) >> C:\Users\NRCF\AppData\Local\Temp\bd661ff7-fc98-42a5-a358-5dacf38eaece.log 2>&1"     
>> } catch {    
>>   $_ | Out-File -Append C:\Users\NRCF\AppData\Local\Temp\bd661ff7-fc98-42a5-a358-5dacf38eaece.log
>>   powershell exit 1
>> }
