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
    weight -0.3493643864224666
    color "red"
    edgetype "local_response"
    penwidth 1.3974575456898664
    deviation 1.0
    sign "negative"
    curved 0
  ]
  edge [
    source 2
    target 3
    weight 0.9720975666640059
    color "green"
    edgetype "local_response"
    penwidth 3.8883902666560237
    deviation 1.0
    sign "positive"
    curved 0
  ]
  edge [
    source 3
    target 7
    weight 0.8019031583200263
    color "green"
    edgetype "local_response"
    penwidth 3.2076126332801054
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
    weight 1.1224637157330726
    color "green"
    edgetype "local_response"
    penwidth 4.48985486293229
    deviation 1.0
    sign "positive"
    curved 0
  ]
  edge [
    source 8
    target 9
    weight 0.7928710565298279
    color "green"
    edgetype "local_response"
    penwidth 3.1714842261193117
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
    source 11
    target 4
    weight 0.9356087868905413
    color "green"
    edgetype "local_response"
    penwidth 3.742435147562165
    deviation 1.0
    sign "positive"
    curved 0
  ]
  edge [
    source 12
    target 3
    weight -0.32081707020375894
    color "red"
    edgetype "perturbation"
    penwidth 1.2832682808150357
    deviation 1.0
    sign "negative"
    curved 0
  ]
  edge [
    source 13
    target 7
    weight -0.5209954963667089
    color "red"
    edgetype "perturbation"
    penwidth 2.0839819854668358
    deviation 1.0
    sign "negative"
    curved 0
  ]
  edge [
    source 14
    target 4
    weight -0.21629692098752717
    color "red"
    edgetype "perturbation"
    penwidth 0.8651876839501087
    deviation 1.0
    sign "negative"
    curved 0
  ]
]
