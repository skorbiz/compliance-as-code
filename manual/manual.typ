#set page(
  paper: "a4",
  margin: (x: 2.5cm, y: 3cm),
  header: [
    #set text(size: 9pt)
    #grid(
      columns: (1fr, 1fr),
      align(left)[User Manual],
      align(right)[Version 1.0]
    )
    #line(length: 100%, stroke: 0.5pt)
  ],
  footer: [
    #line(length: 100%, stroke: 0.5pt)
    #set text(size: 9pt)
    #grid(
      columns: (1fr, 1fr),
      align(left)[© #datetime.today().year() Your Company Name],
      align(right)[Page #context counter(page).display("1 of 1", both: true)]
    )
  ],
  numbering: "1",
)

#set text(
  size: 11pt,
)

#set heading(numbering: "1.1")

#align(center)[
  #text(size: 24pt, weight: "bold")[
    User Manual
  ]
  
  #v(0.5em)
  
  #text(size: 16pt)[
    Product Name / Model XXX
  ]
  
  #v(2em)
  
  #image("logo-placeholder.svg", width: 30%)
  
  #v(2em)
  
  #grid(
    columns: (auto, 1fr),
    row-gutter: 0.3em,
    column-gutter: 1em,
    
    [*Version:*], [1.0],
    [*Date:*], [#datetime.today().display("[day] [month repr:long] [year]")],
    [*Language:*], [English],
  )
]

#pagebreak()

#outline(
  title: [Table of Contents],
  indent: auto,
)

#pagebreak()

= Safety Information

#text(weight: "bold", fill: red)[⚠ WARNING]

Read all safety instructions before using this product. Failure to follow these instructions may result in injury or damage.

== General Safety

- Read and understand all instructions before operating the device
- Keep this manual for future reference
- Follow all warnings and instructions marked on the product
- Do not use this product near water or in wet locations
- Ensure proper ventilation around the device
- Do not block any ventilation openings
- Keep away from heat sources such as radiators, heaters, or other heat-producing devices

== Electrical Safety

- Only use the power supply provided with this product
- Do not use damaged power cords or plugs
- Protect power cords from being walked on or pinched
- Unplug the device during lightning storms or when unused for extended periods
- Do not attempt to service the device yourself - refer all servicing to qualified personnel

== Children and Accessibility

- Keep the product and accessories away from children under 3 years
- Supervise children when they are near the product
- Small parts may present a choking hazard

#pagebreak()

= Introduction

== About This Manual

This user manual provides instructions for the safe installation, operation, and maintenance of your product. Please read this manual carefully before using the device.

For the most up-to-date version of this manual and additional resources, please visit:

#align(center)[
  #link("https://www.example.com/support")[
    #text(size: 12pt, fill: blue)[www.example.com/support]
  ]
]

== Product Overview

This product is designed to [brief description of product purpose and main features].

Key features include:
- Feature 1: Description
- Feature 2: Description  
- Feature 3: Description
- Feature 4: Description

== Package Contents

Please verify that your package contains the following items:

#set enum(numbering: "1.")

+ Main device unit
+ Power adapter and cable
+ User manual (this document)
+ Quick start guide
+ Warranty card
+ [Additional accessories as applicable]

If any items are missing or damaged, please contact your supplier immediately.

#pagebreak()

= Product Specifications

#table(
  columns: (auto, 1fr),
  stroke: 0.5pt,
  align: (left, left),
  
  [*Parameter*], [*Specification*],
  [Model], [Model-XXX],
  [Dimensions (W×D×H)], [XXX × XXX × XXX mm],
  [Weight], [XXX g / XXX kg],
  [Input Voltage], [100-240V AC, 50/60Hz],
  [Power Consumption], [XX W (typical), XX W (maximum)],
  [Operating Temperature], [0°C to 40°C (32°F to 104°F)],
  [Storage Temperature], [-20°C to 60°C (-4°F to 140°F)],
  [Humidity], [10% to 90% RH (non-condensing)],
  [Certifications], [CE, RoHS, [others as applicable]],
)

#pagebreak()

= Installation

== Before Installation

Before installing the device, ensure:
- You have read the safety information in Section 1
- The installation location meets the environmental requirements
- All necessary cables and accessories are available
- You have adequate space for ventilation and access

== Installation Steps

+ *Choose a suitable location*
  - Place on a stable, level surface
  - Ensure adequate ventilation (minimum 10cm clearance on all sides)
  - Avoid direct sunlight, heat sources, and moisture
  - Keep away from electromagnetic interference sources

+ *Connect power supply*
  - Use only the provided power adapter
  - Ensure the power outlet matches the adapter specifications
  - Connect the power cable firmly to the device

+ *Perform initial setup*
  - [Specific setup steps for your device]
  - [Configuration procedures]
  - [Network/connectivity setup if applicable]

+ *Verify installation*
  - Power on the device
  - Check that indicator lights show normal operation
  - Verify basic functionality

#pagebreak()

= Operation

== Getting Started

Detailed operating instructions:

+ Power on the device using [power button/switch location]
+ Wait for initialization (approximately XX seconds)
+ [Step-by-step operation guide specific to your product]

== Normal Operation

=== Basic Functions

[Describe basic operational procedures]

=== Advanced Features

[Describe advanced features and their usage]

== LED Indicators

The device includes the following status indicators:

#table(
  columns: (auto, auto, 1fr),
  stroke: 0.5pt,
  
  [*LED*], [*Color/Pattern*], [*Meaning*],
  [Power], [Green (solid)], [Device is powered on],
  [Power], [Off], [Device is off],
  [Status], [Green (blinking)], [Normal operation],
  [Status], [Red (solid)], [Error condition],
  [Status], [Amber], [Standby mode],
)

#pagebreak()

= Maintenance

== Regular Maintenance

To ensure optimal performance and longevity:

- Clean the exterior regularly with a soft, dry cloth
- Do not use liquid cleaners, sprays, or solvents
- Check cables and connections periodically for wear or damage
- Ensure ventilation openings remain clear and dust-free
- Perform firmware updates as recommended

== Cleaning

+ Power off and unplug the device before cleaning
+ Use a soft, lint-free cloth slightly dampened with water
+ Do not spray liquids directly onto the device
+ Ensure the device is completely dry before reconnecting power
+ Clean ventilation openings with a soft brush or vacuum (low power)

== Storage

If storing the device for an extended period:

- Clean the device thoroughly
- Disconnect all cables
- Store in a cool, dry location
- Use original packaging if possible
- Avoid stacking heavy items on top

#pagebreak()

= Troubleshooting

== Common Issues and Solutions

#table(
  columns: (1fr, 2fr),
  stroke: 0.5pt,
  align: (left, left),
  
  [*Problem*], [*Solution*],
  
  [Device won't power on], [
    • Check power cable connections \
    • Verify outlet is functioning \
    • Check power adapter LED \
    • Contact support if problem persists
  ],
  
  [Device overheating], [
    • Ensure adequate ventilation \
    • Check for blocked air vents \
    • Reduce ambient temperature \
    • Power off and allow to cool
  ],
  
  [Error indicator lit], [
    • Note error pattern/code \
    • Power cycle the device \
    • Refer to error codes section \
    • Contact technical support
  ],
  
  [Performance degradation], [
    • Check for firmware updates \
    • Verify proper installation \
    • Clean ventilation areas \
    • Reset to factory settings
  ],
)

== When to Contact Support

Contact technical support if:
- The device does not function after following troubleshooting steps
- You observe physical damage to the device
- Error messages persist after attempting solutions
- The device exhibits unusual behavior or sounds

#pagebreak()

= Regulatory Information

== EU Declaration of Conformity

This product complies with the essential requirements and other relevant provisions of applicable EU directives. The full EU Declaration of Conformity is available upon request or can be downloaded from our website.

Applicable directives:
- Directive 2014/30/EU (EMC)
- Directive 2014/35/EU (LVD)
- Directive 2011/65/EU (RoHS)
- Directive 2012/19/EU (WEEE)

== FCC Compliance (USA)

This device complies with Part 15 of the FCC Rules. Operation is subject to the following two conditions: (1) this device may not cause harmful interference, and (2) this device must accept any interference received, including interference that may cause undesired operation.

== Disposal and Recycling

#image("weee-symbol.svg", width: 10%)

This symbol indicates that this product should not be disposed of with regular household waste. It must be disposed of at a designated collection point for recycling electrical and electronic equipment. By ensuring proper disposal, you help prevent potential negative consequences for the environment and human health.

For information about recycling this product, contact your local waste disposal service or the retailer where you purchased the product.

#pagebreak()

= Warranty and Support

== Limited Warranty

This product is warranted to be free from defects in materials and workmanship for a period of [XX months/years] from the date of original purchase.

This warranty does not cover:
- Normal wear and tear
- Damage caused by misuse, abuse, or negligence
- Damage from unauthorized modification or repair
- Damage from accidents, natural disasters, or power surges
- Cosmetic damage that does not affect functionality

== Technical Support

For technical assistance, please contact us:

#grid(
  columns: (auto, 1fr),
  row-gutter: 0.5em,
  column-gutter: 1em,
  
  [*Website:*], [www.example.com/support],
  [*Email:*], [support\@example.com],
  [*Phone:*], [+XX XXX XXX XXXX],
  [*Support Hours:*], [Monday-Friday, 9:00-17:00 (local time)],
)

== Online Resources

Visit our support website for:
- Latest firmware updates
- FAQ and knowledge base
- Video tutorials
- Downloadable documentation
- Community forums

#pagebreak()

= Appendix

== Glossary

#table(
  columns: (auto, 1fr),
  stroke: 0.5pt,
  align: (left, left),
  
  [*Term*], [*Definition*],
  [CE], [Conformité Européenne - European conformity marking],
  [RoHS], [Restriction of Hazardous Substances],
  [WEEE], [Waste Electrical and Electronic Equipment],
  [FCC], [Federal Communications Commission],
  [EMC], [Electromagnetic Compatibility],
  [LVD], [Low Voltage Directive],
)

== Revision History

#table(
  columns: (auto, auto, 1fr),
  stroke: 0.5pt,
  
  [*Version*], [*Date*], [*Changes*],
  [1.0], [#datetime.today().display("[month repr:short] [year]")], [Initial release],
)

#pagebreak()

= Notes

#v(2em)

_This page is intentionally left blank for user notes._

#v(2em)

#line(length: 100%, stroke: 0.5pt)
#v(0.5em)
#line(length: 100%, stroke: 0.5pt)
#v(0.5em)
#line(length: 100%, stroke: 0.5pt)
#v(0.5em)
#line(length: 100%, stroke: 0.5pt)
#v(0.5em)
#line(length: 100%, stroke: 0.5pt)
#v(0.5em)
#line(length: 100%, stroke: 0.5pt)
#v(0.5em)
#line(length: 100%, stroke: 0.5pt)
#v(0.5em)
#line(length: 100%, stroke: 0.5pt)
#v(0.5em)
#line(length: 100%, stroke: 0.5pt)
#v(0.5em)
#line(length: 100%, stroke: 0.5pt)
