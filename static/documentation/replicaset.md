## Crear las carpetas
```
mkdir -p "\data\rpt\rs0-0"  "\data\rpt\rs0-1" "\data\rpt\rs0-2"
```

## LEVANTAMOS 3 mongod servidor (cada uno en un puerto)
```
mongod --replSet rs0 --port 28017  --dbpath "\data\rpt\rs0-0" --smallfiles --oplogSize 128

mongod --replSet rs0 --port 28018  --dbpath "\data\rpt\rs0-1" --smallfiles --oplogSize 128

mongod --replSet rs0 --port 28019  --dbpath "\data\rpt\rs0-2" --smallfiles --oplogSize 128
```

## CONECTAMOS A UNO DE ELLOS PARA CREAR EL REPLICASET
```
mongo --port 28017
```

## FICHERO CONFIGURACION REPLICASET
```
rsconf = {

  _id: "rs0",

  members: [

   

     _id: 0,

     host: "localhost:28017"

    },

    {

     _id: 1,

     host: "localhost:28018"

    },

    {

     _id: 2,

     host: "localhost:28019"

    }

   ]

}
```

## INICIAR REPLICASET!!
```
rs.initiate( reconf )
```

## REVISAR CONFIGURACION
```
rs.conf()
```

## QUIEN ES EL MASTER
```
db.isMaster()
```

## ESTADO DEL REPLICASET
```
rs.status()
```
## ELIMINAR UN NODO DEL REPLICASET
```
rs.remove("localhost:28018")
```
## AÑADIR UN ARBITRO
```
rs.addArb("localhost:2018")

rs.status()
```
## TIRAR EL REPLICASET (forzar que falle y eleccion)
```
rs.stepDown()
```
#### NO PUEDES
```
show collections

rs.slaveOk()

show collections
```


##COMO CONECTAR CON MONGO (CLIENTE) CON UN REPLICASET
```
mongo "mongodb://localhost:27017,localhost:27018,localhost:27017/prueba?replicaSet=rs0"
```
