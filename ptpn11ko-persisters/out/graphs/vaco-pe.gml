graph [
  directed 1
  node [
    id 0
    label "EGFR"
    type "protein"
    x 75
    y 30
  ]
  node [
    id 1
    label "AKT"
    type "protein"
    x 150
    y 120
  ]
  node [
    id 2
    label "MTOR"
    type "protein"
    x 150
    y 180
  ]
  node [
    id 3
    label "PI3K"
    type "protein"
    x 150
    y 60
  ]
  node [
    id 4
    label "ERK"
    type "protein"
    x 0
    y 120
  ]
  node [
    id 5
    label "MEK"
    type "protein"
    x 0
    y 60
  ]
  node [
    id 6
    label "GSK3AB"
    type "protein"
    x 0
    y 240
  ]
  node [
    id 7
    label "P90RSK"
    type "protein"
    x 0
    y 180
  ]
  node [
    id 8
    label "RPS6"
    type "protein"
    x 150
    y 240
  ]
  node [
    id 9
    label "mek"
    type "perturbation"
    x -41
    y 60
    ptype "inhib"
  ]
  node [
    id 10
    label "pi3k"
    type "perturbation"
    x 187
    y 60
    ptype "inhib"
  ]
  node [
    id 11
    label "akt"
    type "perturbation"
    x 93
    y 120
    ptype "inhib"
  ]
  node [
    id 12
    label "egf"
    type "perturbation"
    x 75
    y -30
    ptype "stim"
  ]
  node [
    id 13
    label "erk"
    type "perturbation"
    x 56
    y 120
    ptype "inhib"
  ]
  node [
    id 14
    label "braf"
    type "perturbation"
    x -41
    y -15
    ptype "inhib"
  ]
  node [
    id 15
    label "nrg1"
    type "perturbation"
    x 112
    y -30
    ptype "stim"
  ]
  node [
    id 16
    label "hgf"
    type "perturbation"
    x 37
    y -30
    ptype "stim"
  ]
  edge [
    source 0
    target 1
    weight 0.0
    color "red"
    edgetype "local_response"
    penwidth 0.0
    deviation 1.0
    sign "negative"
  ]
  edge [
    source 0
    target 5
    weight 5.705726294685709
    color "green"
    edgetype "local_response"
    penwidth 11.411452589371418
    deviation 1.0
    sign "positive"
  ]
  edge [
    source 0
    target 3
    weight 0.35148920643411186
    color "gray"
    edgetype "local_response"
    penwidth 0.7029784128682237
    deviation -0.0
    sign "positive"
  ]
  edge [
    source 1
    target 6
    weight 0.2554152245758
    color "gray"
    edgetype "local_response"
    penwidth 0.5108304491516
    deviation -0.0
    sign "positive"
  ]
  edge [
    source 1
    target 2
    weight 0.1524748416284562
    color "gray"
    edgetype "local_response"
    penwidth 0.3049496832569124
    deviation -0.0
    sign "positive"
  ]
  edge [
    source 2
    target 1
    weight 2.657003361318443
    color "gray"
    edgetype "local_response"
    penwidth 5.314006722636886
    deviation -0.0
    sign "positive"
  ]
  edge [
    source 2
    target 8
    weight 0.5106999912346281
    color "gray"
    edgetype "local_response"
    penwidth 1.0213999824692561
    deviation -0.0
    sign "positive"
  ]
  edge [
    source 3
    target 1
    weight 0.04208284453078433
    color "gray"
    edgetype "local_response"
    penwidth 0.08416568906156865
    deviation -0.0
    sign "positive"
  ]
  edge [
    source 4
    target 0
    weight 0.0
    color "gray"
    edgetype "local_response"
    penwidth 0.0
    deviation -0.0
    sign "negative"
  ]
  edge [
    source 4
    target 5
    weight -2.165690992856635
    color "red"
    edgetype "local_response"
    penwidth 4.33138198571327
    deviation 1.0
    sign "negative"
  ]
  edge [
    source 4
    target 7
    weight 0.45744680339033406
    color "gray"
    edgetype "local_response"
    penwidth 0.9148936067806681
    deviation -0.0
    sign "positive"
  ]
  edge [
    source 4
    target 8
    weight 0.4686499507367213
    color "gray"
    edgetype "local_response"
    penwidth 0.9372999014734426
    deviation -0.0
    sign "positive"
  ]
  edge [
    source 5
    target 4
    weight 0.11829788471035485
    color "gray"
    edgetype "local_response"
    penwidth 0.2365957694207097
    deviation -0.0
    sign "positive"
  ]
  edge [
    source 7
    target 6
    weight 0.3499569771966158
    color "gray"
    edgetype "local_response"
    penwidth 0.6999139543932316
    deviation -0.0
    sign "positive"
  ]
  edge [
    source 8
    target 2
    weight 0.24053465650849404
    color "gray"
    edgetype "local_response"
    penwidth 0.4810693130169881
    deviation -0.0
    sign "positive"
  ]
  edge [
    source 8
    target 3
    weight 0.0
    color "gray"
    edgetype "local_response"
    penwidth 0.0
    deviation -0.0
    sign "negative"
  ]
  edge [
    source 9
    target 4
    weight -0.6107131658627882
    color "gray"
    edgetype "perturbation"
    penwidth 1.2214263317255765
    deviation -0.0
    sign "negative"
  ]
  edge [
    source 10
    target 1
    weight -2.726285285133696
    color "gray"
    edgetype "perturbation"
    penwidth 5.452570570267392
    deviation -0.0
    sign "negative"
  ]
  edge [
    source 11
    target 1
    weight -2.1721330886829584
    color "red"
    edgetype "perturbation"
    penwidth 4.344266177365917
    deviation 1.0
    sign "negative"
  ]
  edge [
    source 12
    target 0
    weight 0.35346533957009985
    color "gray"
    edgetype "perturbation"
    penwidth 0.7069306791401997
    deviation -0.0
    sign "positive"
  ]
  edge [
    source 13
    target 4
    weight -0.44794153826994565
    color "gray"
    edgetype "perturbation"
    penwidth 0.8958830765398913
    deviation -0.0
    sign "negative"
  ]
  edge [
    source 14
    target 5
    weight -0.9031237865378835
    color "red"
    edgetype "perturbation"
    penwidth 1.806247573075767
    deviation 1.0
    sign "negative"
  ]
  edge [
    source 15
    target 1
    weight 1.8349390087047661
    color "gray"
    edgetype "perturbation"
    penwidth 3.6698780174095322
    deviation -0.0
    sign "positive"
  ]
  edge [
    source 15
    target 5
    weight 1.8110370661689668
    color "green"
    edgetype "perturbation"
    penwidth 3.6220741323379335
    deviation 1.0
    sign "positive"
  ]
  edge [
    source 15
    target 3
    weight 0.15074871870617315
    color "gray"
    edgetype "perturbation"
    penwidth 0.3014974374123463
    deviation -0.0
    sign "positive"
  ]
  edge [
    source 16
    target 1
    weight 0.2971543791020855
    color "gray"
    edgetype "perturbation"
    penwidth 0.594308758204171
    deviation -0.0
    sign "positive"
  ]
  edge [
    source 16
    target 5
    weight 0.8362983595226302
    color "gray"
    edgetype "perturbation"
    penwidth 1.6725967190452604
    deviation -0.0
    sign "positive"
  ]
  edge [
    source 16
    target 3
    weight 0.0
    color "gray"
    edgetype "perturbation"
    penwidth 0.0
    deviation -0.0
    sign "negative"
  ]
]
