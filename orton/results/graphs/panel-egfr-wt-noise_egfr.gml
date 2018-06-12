graph [
  directed 1
  node [
    id 0
    label "PI3K"
    type "protein"
    x -35
    y 60
  ]
  node [
    id 1
    label "AKT"
    type "protein"
    x -35
    y 90
  ]
  node [
    id 2
    label "RAP1"
    type "protein"
    x 35
    y 60
  ]
  node [
    id 3
    label "BRAF"
    type "protein"
    x 35
    y 90
  ]
  node [
    id 4
    label "RAS"
    type "protein"
    x 0
    y 60
  ]
  node [
    id 5
    label "EGFR"
    type "protein"
    x 0
    y 0
  ]
  node [
    id 6
    label "C3G"
    type "protein"
    x 35
    y 30
  ]
  node [
    id 7
    label "ERK"
    type "protein"
    x 0
    y 150
  ]
  node [
    id 8
    label "MEK"
    type "protein"
    x 0
    y 120
  ]
  node [
    id 9
    label "P90RSK"
    type "protein"
    x -35
    y 150
  ]
  node [
    id 10
    label "RAF1"
    type "protein"
    x 0
    y 90
  ]
  node [
    id 11
    label "SOS"
    type "protein"
    x 0
    y 30
  ]
  node [
    id 12
    label "BRAF KD"
    type "perturbation"
    x 61
    y 75
  ]
  node [
    id 13
    label "MEK KD"
    type "perturbation"
    x 26
    y 105
  ]
  edge [
    source 0
    target 1
    weight 0.4007615889811685
    color "light-gray"
    edgetype "local_response"
    penwidth 1.603046355924674
    deviation 0.0
    sign "positive"
    curved 0
  ]
  edge [
    source 1
    target 10
    weight -0.3656013586870993
    color "light-gray"
    edgetype "local_response"
    penwidth 1.4624054347483972
    deviation 0.0
    sign "negative"
    curved 0
  ]
  edge [
    source 2
    target 3
    weight 2.104871977829365
    color "green"
    edgetype "local_response"
    penwidth 8.41948791131746
    deviation 1.0
    sign "positive"
    curved 0
  ]
  edge [
    source 2
    target 8
    weight 0.43976077140368447
    color "green"
    edgetype "local_response"
    penwidth 1.7590430856147379
    deviation 1.0
    sign "positive"
    curved 0
  ]
  edge [
    source 3
    target 8
    weight 0.8557399259927715
    color "light-gray"
    edgetype "local_response"
    penwidth 3.422959703971086
    deviation 0.0
    sign "positive"
    curved 0
  ]
  edge [
    source 4
    target 3
    weight 0.22921404922511968
    color "light-gray"
    edgetype "local_response"
    penwidth 0.9168561969004787
    deviation 0.0
    sign "positive"
    curved 0
  ]
  edge [
    source 4
    target 10
    weight 1.0419015812209118
    color "light-gray"
    edgetype "local_response"
    penwidth 4.167606324883647
    deviation 0.0
    sign "positive"
    curved 0
  ]
  edge [
    source 5
    target 6
    weight 0.2938032848632335
    color "green"
    edgetype "local_response"
    penwidth 1.175213139452934
    deviation 1.0
    sign "positive"
    curved 0
  ]
  edge [
    source 5
    target 0
    weight 0.1272867021783731
    color "light-gray"
    edgetype "local_response"
    penwidth 0.5091468087134924
    deviation 0.0
    sign "positive"
    curved 0
  ]
  edge [
    source 5
    target 11
    weight 1.1448925134731724
    color "light-gray"
    edgetype "local_response"
    penwidth 4.57957005389269
    deviation 0.0
    sign "positive"
    curved 0
  ]
  edge [
    source 6
    target 7
    weight 0.4420199640564516
    color "green"
    edgetype "local_response"
    penwidth 1.7680798562258064
    deviation 1.0
    sign "positive"
    curved 0
  ]
  edge [
    source 6
    target 2
    weight 0.9357562547971711
    color "light-gray"
    edgetype "local_response"
    penwidth 3.7430250191886842
    deviation 0.0
    sign "positive"
    curved 0
  ]
  edge [
    source 7
    target 9
    weight 0.38762012910713595
    color "green"
    edgetype "local_response"
    penwidth 1.5504805164285438
    deviation 1.0
    sign "positive"
    curved 0
  ]
  edge [
    source 8
    target 7
    weight 0.3629214043244524
    color "green"
    edgetype "local_response"
    penwidth 1.4516856172978096
    deviation 1.0
    sign "positive"
    curved 0
  ]
  edge [
    source 9
    target 11
    weight -0.8355885430478303
    color "light-gray"
    edgetype "local_response"
    penwidth 3.342354172191321
    deviation 0.0
    sign "negative"
    curved 1
  ]
  edge [
    source 11
    target 4
    weight 0.9874613732804537
    color "light-gray"
    edgetype "local_response"
    penwidth 3.9498454931218148
    deviation 0.0
    sign "positive"
    curved 0
  ]
  edge [
    source 12
    target 3
    weight -0.7922576712343027
    color "red"
    edgetype "perturbation"
    penwidth 3.1690306849372107
    deviation 1.0
    sign "negative"
    curved 0
  ]
  edge [
    source 13
    target 8
    weight -0.7527601115781062
    color "red"
    edgetype "perturbation"
    penwidth 3.0110404463124247
    deviation 1.0
    sign "negative"
    curved 0
  ]
]
