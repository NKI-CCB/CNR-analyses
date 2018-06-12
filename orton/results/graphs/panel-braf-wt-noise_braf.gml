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
    label "SOS"
    type "protein"
    x 0
    y 30
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
    label "MEK"
    type "protein"
    x 0
    y 120
  ]
  node [
    id 8
    label "ERK"
    type "protein"
    x 0
    y 150
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
    label "RAS"
    type "protein"
    x 0
    y 60
  ]
  node [
    id 12
    label "BRAF KD"
    type "perturbation"
    x 61
    y 75
  ]
  edge [
    source 0
    target 1
    weight 0.44693116936465593
    color "light-gray"
    edgetype "local_response"
    penwidth 1.7877246774586237
    deviation -0.0
    sign "positive"
    curved 0
  ]
  edge [
    source 1
    target 10
    weight -0.34147110936137426
    color "light-gray"
    edgetype "local_response"
    penwidth 1.365884437445497
    deviation 0.0
    sign "negative"
    curved 0
  ]
  edge [
    source 3
    target 7
    weight 0.07795264570496277
    color "green"
    edgetype "local_response"
    penwidth 0.3118105828198511
    deviation 1.0
    sign "positive"
    curved 0
  ]
  edge [
    source 4
    target 3
    weight 0.07067149879042137
    color "light-gray"
    edgetype "local_response"
    penwidth 0.28268599516168547
    deviation 0.0
    sign "positive"
    curved 0
  ]
  edge [
    source 4
    target 11
    weight 1.024179156153121
    color "light-gray"
    edgetype "local_response"
    penwidth 4.096716624612484
    deviation 0.0
    sign "positive"
    curved 0
  ]
  edge [
    source 5
    target 6
    weight 0.9191907372250194
    color "light-gray"
    edgetype "local_response"
    penwidth 3.6767629489000777
    deviation 0.0
    sign "positive"
    curved 0
  ]
  edge [
    source 5
    target 0
    weight 0.2287930652539457
    color "light-gray"
    edgetype "local_response"
    penwidth 0.9151722610157828
    deviation 0.0
    sign "positive"
    curved 0
  ]
  edge [
    source 5
    target 2
    weight 0.17744631889820073
    color "light-gray"
    edgetype "local_response"
    penwidth 0.7097852755928029
    deviation 0.0
    sign "positive"
    curved 0
  ]
  edge [
    source 5
    target 4
    weight 0.9420127688437043
    color "light-gray"
    edgetype "local_response"
    penwidth 3.7680510753748173
    deviation 0.0
    sign "positive"
    curved 0
  ]
  edge [
    source 6
    target 2
    weight 0.8590219658678147
    color "light-gray"
    edgetype "local_response"
    penwidth 3.4360878634712586
    deviation 0.0
    sign "positive"
    curved 0
  ]
  edge [
    source 7
    target 8
    weight 0.07380219050260792
    color "green"
    edgetype "local_response"
    penwidth 0.29520876201043167
    deviation 1.0
    sign "positive"
    curved 0
  ]
  edge [
    source 8
    target 9
    weight 0.3456940675799459
    color "green"
    edgetype "local_response"
    penwidth 1.3827762703197837
    deviation 1.0
    sign "positive"
    curved 0
  ]
  edge [
    source 9
    target 4
    weight -0.7939641725695621
    color "light-gray"
    edgetype "local_response"
    penwidth 3.1758566902782484
    deviation 0.0
    sign "negative"
    curved 1
  ]
  edge [
    source 11
    target 10
    weight 1.0227787787730518
    color "light-gray"
    edgetype "local_response"
    penwidth 4.091115115092207
    deviation 0.0
    sign "positive"
    curved 0
  ]
  edge [
    source 12
    target 3
    weight -0.8038230495745265
    color "red"
    edgetype "perturbation"
    penwidth 3.215292198298106
    deviation 1.0
    sign "negative"
    curved 0
  ]
]
