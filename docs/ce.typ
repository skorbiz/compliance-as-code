#set page(paper: "a4", margin: (x: 2.5cm, y: 2.5cm))
#set text(size: 11pt)

#align(center)[
  #text(size: 18pt, weight: "bold")[EU DECLARATION OF CONFORMITY]
]

#v(1em)

#grid(
  columns: (1fr, 1fr),
  [
    *Manufacturer:*\
    Your Company Name\
    Address Line 1\
    Country
  ],
  [
    *Date of Issue:*\
    #datetime.today().display("[day] [month repr:long] [year]")
  ]
)

#v(2em)

= Product Information

#table(
  columns: (auto, 1fr),
  stroke: none,
  [*Product Name:*], [Your Product Name],
  [*Model/Type:*], [Model-XXX],
  [*Serial Number:*], [SN-XXXXXXX],
)

#v(2em)

= Declaration

This declaration of conformity is issued under the sole responsibility of the manufacturer.

The product is in conformity with the following Union harmonisation legislation:

- Directive 2014/30/EU - Electromagnetic Compatibility (EMC)
- Directive 2014/35/EU - Low Voltage Directive (LVD)
- Regulation (EU) 2024/2847 - Cyber Resilience Act (CRA)

#v(2em)

= Harmonised Standards Applied

- EN 55032:2015 - EMC of multimedia equipment
- EN 62368-1:2014 - Audio/video and ICT equipment safety

#v(3em)

#grid(
  columns: (1fr, 1fr),
  [
    *Place:* \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\
    *Date:* \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
  ],
  [
    *Signature:* \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\
    *Name:* \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
  ]
)
