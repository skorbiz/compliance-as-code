#set page(
  paper: "a4",
  margin: (x: 2.5cm, y: 2.5cm),
)

#set text(
  size: 11pt,
)

#align(center)[
  #text(size: 18pt, weight: "bold")[
    EU DECLARATION OF CONFORMITY
  ]
]

#v(1em)

#grid(
  columns: (1fr, 1fr),
  gutter: 1em,
  
  [
    *Manufacturer:*\
    Your Company Name\
    Address Line 1\
    Address Line 2\
    Country
  ],
  
  [
    *Date of Issue:*\
    #datetime.today().display("[day] [month repr:long] [year]")
  ]
)

#v(2em)

= Product Information

#grid(
  columns: (auto, 1fr),
  row-gutter: 0.5em,
  column-gutter: 1em,
  
  [*Product Name:*], [Your Product Name],
  [*Model/Type:*], [Model-XXX],
  [*Serial Number:*], [SN-XXXXXXX],
  [*Batch/Lot Number:*], [Batch-2026-001],
)

#v(2em)

= Declaration

This declaration of conformity is issued under the sole responsibility of the manufacturer.

The object of the declaration described above is in conformity with the following Union harmonisation legislation:

#v(1em)

#set list(indent: 1em)

- Directive 2014/30/EU - Electromagnetic Compatibility (EMC)
- Directive 2014/35/EU - Low Voltage Directive (LVD)  
- Directive 2011/65/EU - Restriction of Hazardous Substances (RoHS)
- Directive 2012/19/EU - Waste Electrical and Electronic Equipment (WEEE)

#v(2em)

= Harmonised Standards Applied

The following harmonised standards and technical specifications have been applied:

#v(1em)

- EN 55032:2015 - Electromagnetic compatibility of multimedia equipment
- EN 55035:2017 - Electromagnetic compatibility of multimedia equipment
- EN 61000-3-2:2014 - Harmonic current emissions
- EN 61000-3-3:2013 - Voltage changes, voltage fluctuations and flicker
- EN 62368-1:2014 - Audio/video and ICT equipment safety

#v(2em)

= Additional Information

#grid(
  columns: (auto, 1fr),
  row-gutter: 0.5em,
  column-gutter: 1em,
  
  [*Notified Body:*], [N/A],
  [*Certificate Number:*], [N/A],
  [*Technical File:*], [Held at manufacturer's address],
)

#v(3em)

#grid(
  columns: (1fr, 1fr),
  gutter: 2em,
  
  [
    *Place:*\
    \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
    
    #v(2em)
    
    *Date:*\
    \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
  ],
  
  [
    *Signature:*\
    #v(1em)
    \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
    
    #v(1em)
    
    *Name:*\
    \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
    
    #v(0.5em)
    
    *Position:*\
    \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
  ]
)

#v(2em)

#align(center)[
  #text(size: 9pt, style: "italic")[
    This declaration is valid only for the products as described above and under the conditions specified herein.
  ]
]
