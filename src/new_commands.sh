#una manera de enviar un query, sin especificar el nombre de la tabla
uws --host https://www.cosmosim.org/uws/query --user forero --password PASS job new queue="long" query="select fofId, mass, np from Bolshoi.FOF m where m.x < 100 and m.y < 100 and m.z < 100 and m.np>200 and snapnum=416" --run

uws --host https://www.cosmosim.org/uws/query --user forero --password PASS job results 1456346181138577476 csv

#otra manera pero dando el nombre de la tabla
uws --host https://www.cosmosim.org/uws/query --user forero --password PASS job new queue="long" query="select x,y,z from MDR1.FOF where snapnum=85 order by mass desc limit 20" table="nombre_tabla" --run

uws --host https://www.cosmosim.org/uws/query --user forero --password PASS job results nombre_tabla csv

