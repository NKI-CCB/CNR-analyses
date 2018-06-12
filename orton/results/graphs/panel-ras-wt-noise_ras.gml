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
  node [
    id 14
    label "RAS KD"
    type "perturbation"
    x 26
    y 45
  ]
  edge [
    source 0
    target 1
    weight 0.46686466577586927
    color "light-gray"
    edgetype "local_response"
    penwidth 1.867458663103477
    deviation 0.0
    sign "positive"
    curved 0
  ]
  edge [
    source 1
    target 10
    weight -0.9522263942599103
    color "red"
    edgetype "local_response"
    penwidth 3.808905577039641
    deviation 1.0
    sign "negative"
    curved 0
  ]
  edge [
    source 3
    target 7
    weight 0.09106641045224646
    color "green"
    edgetype "local_response"
    penwidth 0.36426564180898585
    deviation 1.0
    sign "positive"
    curved 0
  ]
  edge [
    source 4
    target 3
    weight 0.16976915320183472
    color "light-gray"
    edgetype "local_response"
    penwidth 0.6790766128073389
    deviation 0.0
    sign "positive"
    curved 0
  ]
  edge [
    source 4
    target 10
    weight 1.0379894946030659
    color "light-gray"
    edgetype "local_response"
    penwidth 4.1519579784122636
    deviation 0.0
    sign "positive"
    curved 0
  ]
  edge [
    source 5
    target 6
    weight 1.0981690927977101
    color "light-gray"
    edgetype "local_response"
    penwidth 4.3926763711908405
    deviation 0.0
    sign "positive"
    curved 0
  ]
  edge [
    source 5
    target 0
    weight 0.15651426672314162
    color "light-gray"
    edgetype "local_response"
    penwidth 0.6260570668925665
    deviation 0.0
    sign "positive"
    curved 0
  ]
  edge [
    source 5
    target 2
    weight 0.335130837248751
    color "light-gray"
    edgetype "local_response"
    penwidth 1.340523348995004
    deviation 0.0
    sign "positive"
    curved 0
  ]
  edge [
    source 5
    target 11
    weight 1.2963190441855792
    color "light-gray"
    edgetype "local_response"
    penwidth 5.185276176742317
    deviation 0.0
    sign "positive"
    curved 0
  ]
  edge [
    source 6
    target 2
    weight 0.8590225959664878
    color "light-gray"
    edgetype "local_response"
    penwidth 3.436090383865951
    deviation 0.0
    sign "positive"
    curved 0
  ]
  edge [
    source 7
    target 8
    weight 0.06709289802161797
    color "green"
    edgetype "local_response"
    penwidth 0.2683715920864719
    deviation 1.0
    sign "positive"
    curved 0
  ]
  edge [
    source 8
    target 9
    weight 0.41886164431858414
    color "green"
    edgetype "local_response"
    penwidth 1.6754465772743365
    deviation 1.0
    sign "positive"
    curved 0
  ]
  edge [
    source 9
    target 11
    weight -0.9424149227516381
    color "light-gray"
    edgetype "local_response"
    penwidth 3.7696596910065523
    deviation 0.0
    sign "negative"
    curved 1
  ]
  edge [
    source 12
    target 3
    weight -0.818150358441928
    color "red"
    edgetype "perturbation"
    penwidth 3.272601433767712
    deviation 1.0
    sign "negative"
    curved 0
  ]
  edge [
    source 13
    target 7
    weight -0.7359366828715281
    color "red"
    edgetype "perturbation"
    penwidth 2.9437467314861125
    deviation 1.0
    sign "negative"
    curved 0
  ]
  edge [
    source 14
    target 4
    weight -0.6654017239717855
    color "red"
    edgetype "perturbation"
    penwidth 2.661606895887142
    deviation 1.0
    sign "negative"
    curved 0
  ]
]
