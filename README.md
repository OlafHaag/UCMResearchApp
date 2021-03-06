# NeuroPsy Research App
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


<a href='https://play.google.com/store/apps/details?id=com.olafhaag.neuropsyresearch&pcampaignid=pcampaignidMKT-Other-global-all-co-prtnr-py-PartBadge-Mar2515-1'><img alt='Get it on Google Play' src='https://play.google.com/intl/en_us/badges/static/images/badges/en_badge_web_generic.png'/></a>

This app should serve as a starting point for neuropsychological research on mobile devices.  
The necessity for conducting research outside of a laboratory became more paramount during the COVID-19 pandemic when 
face-to-face contact was restricted as a safety measure.
 
## Background
This app demonstrates a toy example for the uncontrolled manifold (UCM) hypothesis (Scholz & Schöner, 1999).
In its basic form there is one performance criterion for a task, but two degrees of freedom (df) to fulfill that goal.

target = x1 + x2  | target = const  
x1 and x2 are two uncoupled state variables.

This creates a subspace of df configurations that is redundant for successful task performance.

[//]: # (Todo: Is that really a vector SUBSPACE with all its properties?)

Final state variability in df configurations should be elongated along the task-irrelevant direction and be less in the
task-relevant direction orthogonal to it.

This is a toy example as it doesn't really explore the variability in the underlying biomechanical system and only
captures results of the control signals. I assume, there's no measurable effect of control-dependent noise either.

Since optimal feedback control is related to UCM theory in the sense that the optimal control law may not act along
certain dimensions (the UCM), one prediction made for optimal feedback control in the presence of control-dependent
noise is that if more control is asserted in the redundant direction (e.g. no optimal control law) the reduced variance
in that direction comes at the expense of increased variance in the task-relevant direction (Todorov, 2004).

To demonstrate one possible operationalization for testing that prediction, there's one task condition that tries to
limit the variability compared to the redundant direction of the unconstrained task by introducing a second performance
criterion that relies on one of the degrees of freedom.
As mentioned, due to suppositional absence of measurable effects of control-dependent noise, no increased error in the
first performance criterion is expected.

## References
John P. Scholz; Gregor Schöner (1999).
"The uncontrolled manifold concept: identifying control variables for a functional task".
Experimental Brain Research. 126 (3): 289–306.

Todorov, Emmanuel (2004). "Optimality principles in sensorimotor control". Nature Neuroscience. 7 (9): 907–915.


## Installation
- Available on Google Play: https://play.google.com/store/apps/details?id=com.olafhaag.neuropsyresearch  
OR 
- compile using buildozer
- Install apk to Android device

## Translation
- Use PoEdit to extract strings wrapped in _("...") function calls.
- In PoEdit add a new extractor for the kivy language files.
- To export the Terms of Use and Privacy Policy to markdown files for all translated languages, run the terms.py and privacypolicy.py files respectively.

## Legal attribution
Google Play and the Google Play logo are trademarks of Google LLC.
