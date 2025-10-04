# USING SATELLITES FOR RADAR PERFORMANCE MONITORING AND CALIBRATION

**DOCUMENT 753-95**

## Commanders Council

**JOINT RANGE INSTRUMENTATION ACCURACY IMPROVEMENT GROUP**

### Participating Organizations

- WHITE SANDS MISSILE RANGE
- KWAJALEIN MISSILE RANGE
- YUMA PROVING GROUND
- DUGWAY PROVING GROUND
- COMBAT SYSTEMS TEST ACTIVITY
- ATLANTIC FLEET WEAPONS TRAINING FACILITY
- NAVAL AIR WARFARE CENTER WEAPONS DIVISION
- NAVAL AIR WARFARE CENTER AIRCRAFT DIVISION
- NAVAL UNDERSEA WARFARE CENTER DIVISION, NEWPORT
- PACIFIC MISSILE RANGE FACILITY
- 30TH SPACE WING
- 45TH SPACE WING
- AIR FORCE FLIGHT TEST CENTER
- AIR FORCE DEVELOPMENT TEST CENTER
- AIR FORCE WEAPONS AND TACTICS CENTER
- SPACE AND MISSILE SYSTEMS CENTER
- SPACE TEST AND EXPERIMENTATION PROGRAM OFFICE
- ARNOLD ENGINEERING DEVELOPMENT CENTER

**DISTRIBUTION A: APPROVED FOR PUBLIC RELEASE; DISTRIBUTION IS UNLIMITED**

**MARCH 1995**

Prepared by:
**JOINT RANGE INSTRUMENTATION ACCURACY IMPROVEMENT GROUP**
**RANGE COMMANDERS COUNCIL**

Published by:
Secretariat, Range Commanders Council
U.S. Army White Sands Missile Range, New Mexico 88002-5110

---

## TABLE OF CONTENTS

**Page**

- Acronyms and Initialisms ... vi
- Introduction ... 1
- Radar Calibration and Performance Monitoring Definitions ... 1
  - Radar Calibration ... 1
  - Radar Performance Monitoring ... 2
- Historical Background ... 3
- Track Data Evaluation Methods ... 5
  - The BET Method ... 5
  - The ORACLE/ORCA Method ... 6
  - The Ephemeris Method ... 6
- Methods Advantages and Disadvantages ... 7
  - The BET Method ... 7
  - ORACLE/ORCA Method ... 7
  - The Ephemeris Method ... 8
- Benefits Derived by Using Satellites ... 9
  - Doppler Range-Rate Systems Acceleration Dependent Error ... 10
  - Problems in the FPQ-6 RECS Upgrade ... 11
  - The Nth Time Around Range Problem at Kokee Park ... 11
  - A Doppler System Problem at the MPS-36 ... 11
  - Data Time Tag Error Detection ... 12
- Other Advantages Offered by Satellite Tracking ... 12
- Practical Considerations for Radar Calibration ... 12
  - Scheduling and Pass Selection ... 12
  - NORAD 2 LINE Element Set ... 13
  - Preliminary Pass Predictions ... 13
  - Tracking Considerations ... 17
  - Considerations During Analysis ... 18

### Appendixes

**Page**

- A. Single Revolution ORACLE Accuracy ... A-1
- B. Radar Systems Errors Detected by Tracking Satellites ... B-1

---

## LIST OF FIGURES AND TABLES

### List of Figures

- 1. Rev 07024/T1202/Ephemeris ... 19
- 2. Rev 07024/T1202/Ephemeris ... 20
- 3. Rev 07024/T1202/Ephemeris ... 21
- 4. Rev 07024/T1202/Ephemeris ... 22
- 5. Rev 07024/T1202/Ephemeris ... 23
- B-1. Normal Range Data for FPQ-6 ... B-11
- B-2. Normal Azimuth Data for FPQ-6 ... B-12
- B-3. Normal Elevation Data for FPQ-6 ... B-13
- B-4. Normal Range Rate Data for FPQ-6 ... B-14
- B-5. Azimuth Misalignment Error (FPS-16) ... B-15
- B-5A. Azimuth Misalignment Error (FPS-16) ... B-16
- B-6. Droop Error at FPQ-6 ... B-17
- B-6A. Droop Error at FPQ-6 ... B-18
- B-7. Velocity Sensitive Range Rate Error (MPS-36) ... B-19
- B-8. Doppler Design Error (HAIR) ... B-20
- B-9. Angle System Oscillation (MPS-36) Azimuth ... B-21
- B-9A. Angle System Oscillation (MPS-36) Elevation ... B-22
- B-10. Intermittent Azimuth Bits (TPQ-18) ... B-23
- B-10A. Intermittent Azimuth Bits (TPQ-18) ... B-24
- B-10B. Intermittent Azimuth Bits (TPQ-18) ... B-25
- B-11. Digital System Error (FPS-16) ... B-26
- B-11A. Digital System Error (HAIR) ... B-27
- B-11B. Digital System Error (TPQ-18) ... B-28
- B-12. Range Error Caused by Tuning (Kokee Park FPS-16) ... B-29
- B-13. Azimuth Misalignment Error (Hill AFB MPS-36) ... B-30
- B-13A. Azimuth Misalignment Error (Hill AFB MPS-36) ... B-31
- B-14. Unusually Large Droop Error (Hill AFB MPS-36) ... B-32
- B-14A. Unusually Large Droop Error (Hill AFB MPS-36) ... B-33
- B-15. Range Problem & Encoder Nonlinearity (Ft Huachuca FPS-16) ... B-34
- B-15A. Range Problem & Encoder Nonlinearity (Ft Huachuca FPS-16) ... B-35
- B-16. Range Problem & Encoder Nonlinearity (Ft Huachuca FPS-16) ... B-36
- B-17. Example of Errors Produced by Oracle Software ... B-37
- B-17A. Example of Errors Produced by Oracle Software ... B-38
- B-18. Survey Errors Detected by Satellite Track ... B-39
- B-18A. Survey Errors Detected by Satellite Track ... B-40
- B-19. Range Machine Problem (Point Mugu FPS-16) ... B-41
- B-19A. Range Machine Problem (Point Mugu FPS-16) ... B-42
- B-20. Timing Problems Identified After Modification (FPQ-6) ... B-43
- B-20A. Timing Problems Identified After Modification (FPQ-6) ... B-44
- B-21. Nth Time Range Problem (Kokee Park FPS-16) ... B-45
- B-22. Range Rate Problem After DLM (TPQ-18) ... B-46
- B-23. Side Lobe Detection Software Not Used (FPQ-14) ... B-47
- B-23A. Side Lobe Detection Software Not Used (FPQ-14) ... B-48

### List of Tables

- A-1. Oracle/RPM Comparison for Hair Radar ... A-4
- A-2. Oracle/RPM Differences ... A-5
- A-3. Oracle/RPM Comparison for FPS-16 #1 ... A-6
- A-4. Oracle/RPM Comparison for FPS-16 #2 ... A-7
- A-5. Oracle/RPM Comparison for FPQ-6 Radar ... A-8
- A-6. Oracle/RPM Comparison for MPS-36 Radar ... A-9
- A-7. Oracle/RPM Comparison for FPQ-14 Radar ... A-10

---

## ACRONYMS AND INITIALISMS

- **AMIS** - Azimuth Misalignment
- **AOS** - Acquisition of Signal
- **ARCS** - Advanced Radar Calibration System
- **AZERO** - Azimuth Encoder Bias
- **BET** - Best Estimate of Trajectory
- **CSP** - Coherent Signal Processor
- **DLM** - Depot Level Maintenance
- **DMA** - Defense Mapping Agency
- **DOD** - Department of Defense
- **DOE** - Department of Energy
- **DVES** - Doppler Velocity Extraction Subsystem
- **EBIAS** - Elevation Bias Errors
- **ECEF** - Earth-Centered, Earth-Fixed
- **ETR** - Eastern Test Range
- **HAIR** - High Accuracy Instrumentation Radar
- **KMR** - Kwajalein Missile Range
- **LOS** - Loss of Signal
- **MIPIR** - Missile Precision Instrumentation Radar
- **MOTR** - Multiple Object Tracking Radar
- **NASA** - National Aeronautics and Space Administration
- **NAVSOC** - Navy Satellite Operations Center
- **NITE** - N-Interval Trajectory Estimation
- **NSWC** - Naval Surface Warfare Center
- **ODC** - Optical Data Corrector
- **PCA** - Point of Closest Approach
- **PMR** - Pacific Missile Range
- **PRF** - Pulse Repetition Frequency
- **RADCAL** - Calibration Satellite
- **RAE** - Radar Range, Azimuth, Elevation
- **Rdot** - Range Rate
- **RECS** - Radar Embedded Computer System
- **REDS** - Radar Error Detection System
- **RF** - Radio Frequency
- **RPM** - Radar Performance Monitoring
- **RV** - Reentry Vehicle
- **SNR** - Signal-to-Noise Ratio
- **TRAM** - Trajectory Reconstruction and Analysis Method
- **WTR** - Western Test Range

---

## Introduction

This document describes the process by which satellites may be used to calibrate and to maintain the performance of metric tracking radar systems. Historical background is included to show why an aggressive radar performance monitoring program became necessary. Various methods are outlined and the advantages of these methods are compared. Practical information is provided to assist in planning and in tracking calibration satellites. Examples of test results are provided to assist the analyst in recognizing errors in data peculiar to metric tracking radars. The examples also illustrate the benefits derived by using an orbiting vehicle for radar performance monitoring, particularly a satellite instrumented with a transponder. Although the methods described have been applied to C-band systems, the principles should be applicable to other tracking radars.

While it may seem unnecessary for a test range to compensate for "small errors" in radar data because of local accuracy requirements, it is quite likely that extreme errors will be discovered by tracking satellites. These errors may degrade metric data to the point where it is unusable. A review of some errors observed at other test ranges (shown in appendix B) is recommended.

## Radar Calibration and Performance Monitoring Definitions

### Radar Calibration

Radar data represent "reality" as corrupted by systematic and random measurement errors. For purposes of data analysis, errors in metric measurements are usually represented mathematically as a linear combination of systematic error terms and a random error component. This mathematical representation is referred to as the "system error model." Systematic errors, by their nature, are repeatable and predictable; that is, any error can be compensated for by application of the system error model, once its form is established and the value of the systematic error model coefficient has been determined. Calibration, in general, then involves the a priori determination of the systematic error model coefficients and the subsequent application of the system error model to predict and to evaluate radar data. If it is possible to correct measurements for systematic errors through the use of the system error model to the extent that the unexplained "residual" deviation from predicted performance is "small" and attributable to random causes, then the radar is said to be "in calibration."

Reduction of observed error magnitudes is the principal way that raw radar measurements can be made more accurate, that is, closer to truth. Therefore, radar calibration refers to the measurement and reduction of the pedestal, antenna, radio frequency (RF) system, and range systematic errors which adversely affect the accuracy of radar data. Some of the more important systematic errors inherent in the radar system consist of pedestal mislevel, antenna droop, RF axis misalignment (antenna feed misalignment or azimuth skew), encoder bias, axis nonorthogonality, encoder nonlinearity, range bias, range-rate bias, and timing bias. These are the measurable errors. Of course, to have fully corrected radar data it is necessary to compensate for other errors such as refraction and transit time. These errors, referred to as propagation dependent errors, are not associated with the radar hardware and are not identified as part of the calibration process.

All radar systematic errors are not measured by tracking satellites. Some are estimated using pedestal mounted optical systems which are aligned to the mechanical (encoder) axis of the pedestal. The optical system is then used to observe the positions of stars, which are used as truth references. Other systematic errors are measured with metrological instruments, and still other errors (including the most difficult to obtain, namely RF errors) are determined by tracking satellites.

As noted previously, since the effect of systematic errors on the data is predictable, the data can be corrected for these errors, so they do not appear in the final metric data product. Depending on facilities at a particular test range, some errors may be corrected at the radar site, so they do not appear in data transmitted in real time. Other errors can be corrected by adjustments to the hardware. This procedure is often referred to as an alignment. However, compensation for most systematic errors is made during post mission processing in software using the mathematical radar error model and the error model coefficients determined in the calibration process. If the radar is working well (that is, functional performance is good) and is well calibrated, the total residual systematic error will be small (for example, less than 10 feet in range and less than 0.05 mils in angles), and the compensated data provided to users will be very accurate.

### Radar Performance Monitoring

Performance monitoring refers to the detection of functional performance problems or unusually large systematic errors resulting in significant degradation of radar data. In most cases, problems in this category result in errors that cannot be corrected mathematically and must be eliminated by correction within the radar system. In many cases, they appear as "surprises" after modifications are made to hardware or software used at the radar site. Resultant problems can be so severe that system functional performance is deficient and range safety, slaving information, and range user final data products are all adversely affected. For example, the radar may not track properly under certain dynamic conditions because of a servo subsystem problem. When the system fails to perform satisfactorily on a functional level, the data may be degraded to the level where it is meaningless to even talk about calibration.

## Historical Background

Prior to 1967 most C-band radars were calibrated by using boresight towers. Although radar data were being used at many ranges to evaluate performance of weapons systems, almost nothing was done by the test ranges to properly measure radar accuracy. At some test ranges, the weapons systems developers questioned the capability of radar systems to provide accurate performance information.

The concern for accuracy led to independent radar calibration programs being established by the Air Force Western Test Range (WTR), Vandenberg Air Force Base, California, and by the Navy Pacific Missile Range (PMR), Point Mugu, California. In 1968, the Navy initiated their program to improve PMR radar accuracy. About this time, the WTR initiated a similar program. The common goal was to develop methods to identify, measure, and correct for errors in radar systems, and both ranges worked together to achieve these goals. To improve radar accuracy, it was necessary to measure several errors which could not be measured with boresight towers. Methods to measure these errors were developed and tests were conducted using metrology equipment such as mirrors, electronic levels, and autocollimators to measure pedestal mislevel, encoder nonlinearity, axis orthogonality, and other pedestal related errors. Film cameras were mounted on radar pedestals and stars were photographed for periods of several hours to measure encoder zero set and optical errors. Afterward RF errors were determined by using the film cameras to record the relative position of a light while tracking a C-band transponder on an instrumented aircraft. By measuring these errors, it was possible to correct radar data post operationally, as part of the data reduction process, and deliver a more accurate product to the end user. By 1971 data from the WTR and PMR were being provided to the user in a corrected format. Techniques developed by the these ranges were later shared with other test ranges operated by the Department of Defense (DOD), the Department of Energy (DOE), and the National Aeronautics and Space Administration (NASA).

In 1972, the Air Force developed the Advanced Radar Calibration System (ARCS) at WTR. The ARCS was used to measure all radar errors automatically and to provide error model coefficients to be used in data reduction. This system made use of a telescope and an Optical Data Corrector (ODC) which was installed on each radar. The ARCS was a significant improvement over the previous methods, because the data collection and processing was automated. A similar system, referred to as Radar Error Detection System (REDS), was later used by the Army at Kwajalein Missile Range (KMR). The ARCS was an important tool, because much was learned about radar errors and their stability. The ARCS made it possible to routinely measure previously difficult errors and provided a standard to evaluate the accuracy of test results obtained by tracking instrumented satellites. Compared to satellite tracking, ARCS had numerous drawbacks. Clear weather was required, scheduling aircraft was difficult, and data processing was costly.

While WTR and PMR were developing methods to measure radar errors using metrology equipment, the Air Force Eastern Test Range (ETR), Patrick Air Force Base, Florida, placed emphasis on the use of satellites for calibration. The ORACLE software was developed by ETR and used to evaluate satellite tracking data from a single radar. The N-Interval Trajectory Estimation (NITE) program was also being used to process data for satellite tracking exercises where multiple radars were employed. During the early years, tracking was limited to radars with large antennas (principally Missile Precision Instrumentation Radar (MIPIR) class radars), because satellites were not equipped with transponders and the quality of data collected by radars with lower loop gain was poor.

Radar calibration was given a real boost with the NASA launch of a geodetic satellite, GEOS-B, in 1968. The GEOS-B was equipped with a C-band transponder to aid in determining the satellite position. Other goals of this launch were:

1. To better determine the accuracy of C-band radar systems,
2. To develop refined methods for calibrating systems,
3. To improve techniques employed in processing radar data,
4. To better determine the geodetic location of the C-band radar sites, and
5. To compare and to correlate results obtained from the C-band radars.

The NASA intended to use its C-band radar systems as well as those from some participating ranges to track the satellite. Several test ranges participated in tracking the transponder and supplying radar data to NASA. Track data was used to generate ephemeris information for the satellite by forming a Best Estimate of Trajectory (BET). Once the BET was formed, it could be compared with radar track data to estimate the accuracy of individual radars.

In 1975, a second geodetic satellite, GEOS-C, was launched. The prime mission of GEOS-C was to measure ocean surface and wave heights using a radar altimeter. Accurate ephemeris data were required for this goal, and a two-frequency Doppler system was carried on board for determining satellite position. The satellite was also equipped with two C-band transponders. The Air Force developed the Radar Performance Monitoring (RPM) software which used the ephemeris data as a standard for comparing radar track data. This ephemeris data, provided by the Defense Mapping Agency (DMA), were accurate to better than 5 meters. Because WTR had previously equipped several radars with ARCS, a large data base consisting of test results was available. The ARCS had already proven it could provide excellent results, and those data were used to validate results obtained from satellite tracks. In addition to the errors normally measured by ARCS, it became possible, on a routine basis, to measure other errors such as elevation and azimuth bias and dynamic lag not previously observable by aircraft.

In using the satellite for calibration purposes, the RPM software compared radar range, azimuth, elevation (RAE), and range-rate (Rdot) measurements with reference standard measurements to the satellite. The comparison is accomplished after transforming the ephemeris data into radar coordinates to the satellite. Such a technique requires accurate time, position, and velocity information. The satellite ephemeris data supplied by DMA became the reference standard for radar calibration with the new RPM software. An initial study on the use of the satellite for radar calibration was completed within 6 months. The study showed that a single radar could be accurately calibrated using satellites, provided accurate ephemeris (position and velocity) derived from Doppler information was available. The software used for processing track data from GEOS-C was later provided to several other ranges.

The GEOS-C was used for radar calibration and performance monitoring until 1985 when GEOSAT, which was equipped with Doppler transmitters for accurate orbit determination, was launched. The prime mission of GEOSAT, like GEOS-C, was to determine ocean heights. The DMA stations tracked GEOSAT and the Doppler data were processed by the Naval Surface Warfare Center (NSWC). The NSWC provided the ephemeris information with the 3- to 5-meter accuracy required for radar calibration purposes. The GEOSAT was used by several of the test ranges until March 1990 when the onboard power system failed. Three years later, RADCAL, the first satellite developed specifically for radar calibration, was launched.

## Track Data Evaluation Methods

Three primary methods are used by test ranges to monitor performance and calibrate radars through the use of satellites: BET, ORACLE/ORCA, and Ephemeris.

### The BET Method

The Best Estimate of Trajectory (BET) is formed from radar track data provided by more than one radar. The BET software for satellite orbit determination can take advantage of constraining the trajectory to follow free-fall equations of motion. Because of this powerful constraint, only the orbital initial position and velocity are estimated. The quality of the BET is dependent on the number of radars used, the geometric location of the radars relative to the satellite pass, the quality of the received signal, and the quality of data produced by the individual radars. This method works well for some ranges where several radars are spread over a large area. The ETR is a good candidate for the successful use of this approach with several radars located between Patrick Air Force Base at the north end and Ascension Island at the south. The benefit of this geometry would be limited to satellites with the proper orbital inclination. The BET is formed by using track data from radars at the ends and other radars located in the Caribbean. Once the BET is formed, each radar is compared with the BET to determine individual performance. Weighting and the radar error model terms to be used for each radar can be assigned by the analyst. If a particular radar appears questionable, the BET can be rerun with this radar weighted out of the solution or a different model may be used. The new BET, no longer adversely influenced by the questionable radar, is then used as the standard for comparison with each of the radars. Examples of software used for this method are NITE, Trajectory Reconstruction and Analysis Method (TRAM), and TRACE.

### The ORACLE/ORCA Method

A second method makes use of software that develops a trajectory based on track data from the radar under test (a single radar), and uses this trajectory to measure errors in the same radar. At first this would appear unreasonable, since the trajectory is produced by the radar which is being tested; however, the orbital constraints mentioned earlier make it possible. In reality the method works within limits. Results of a study to determine accuracy and limitations is provided in appendix A. The ORACLE was developed by the Air Force at ETR in 1969. In this software, the error model coefficients, along with the orbital parameters of the satellite (constrained by Newton's laws of motion), are determined by a simultaneous least-squares solution. Initially ORACLE required a double revolution pass of the same satellite with the second pass occurring one orbital revolution after the first. The software was later modified to use data from a single pass. Both the modified version and the original have been used at WTR. The ETR uses the original version, now called ORCA. The modified version was made available to several other ranges.

Although results can produce fair estimates of some parameters (comparison with other methods will be shown in appendix A), this software is usually used for a "quick estimate" of radar performance. Results are highly dependent on the target being tracked, the pass geometry, and the received signal quality. A more recent variation of this type of software is presently being used at the WTR. This version, known as the CAL program, permits the use of single or multiple stations to better estimate the trajectory for comparison with the individual radars. When multiple site data are input, this new version essentially produces a BET to enhance the quality of the trajectory and consequently the quality of the radar error estimates.

### The Ephemeris Method

This method requires precise ephemeris data as a reference standard. In a typical calibration operation, the radar under test would track a suitable satellite and record time, range, azimuth, elevation, and range-rate data. The comparison of the radar measurements with the precision ephemeris standard then allows evaluation of radar performance by using the predictive system error model. In the case of RADCAL, precision ephemeris can be obtained through processing Doppler data collected by 16 ground stations operated by the DOD, NASA, and DOE ranges, or by 4 stations operated by the Navy Satellite Operations Center (NAVSOC) for Navy Navigation Satellites. Precise ephemeris information available in an earth-centered, earth-fixed coordinate system (ECEF usually denoted by the letters EFG) is obtained from NSWC.

The analyst obtains ephemeris data from NSWC for the particular tracking period, for the radar site of interest, and transforms it to RAE and Rdot coordinates for the radar site being evaluated. As mentioned earlier, the RPM software was developed specifically to make use of this precise ephemeris data.

The RPM is referenced in this discussion, because it is used by or is readily available to all test ranges. The radar track data, satellite ephemeris data, and site location information are used as inputs to the RPM software to compare the reference (computed) RAE data to the RAE and Rdot radar track data. The RPM program provides a listing and a plot of differences. Error estimates, depending upon analyst selection, are also provided as output. Estimated errors are then applied as corrections to the radar data using the system error model and plots of the residual errors are produced.

## Methods Advantages and Disadvantages

### The BET Method

Results obtainable by this method vary depending on radar numbers, radar locations, pass geometry, and signal quality. Accuracy of the error estimates should surpass that using the ORACLE approach (since the BET is formed by using data from several radars) and, under ideal conditions, could approach the ephemeris method. However, accuracy of the BET method can be more variable when compared to using ephemeris, because results are easily affected by analyst experience and judgment. The best solution for the BET is obtained when several radars at different geographical locations are used. Scheduling a sufficient number of radars for simultaneous track may be difficult even though geometry may be ideal at some ranges. Results are not normally obtained for several days because of the time necessary to collect data and make the necessary computer runs; however, at ETR this process has been automated to produce results in much less time.

### ORACLE/ORCA Method

The major advantage of the ORACLE/ORCA method is rapid turnaround for analysis. It is not necessary to wait for ephemeris data. In many cases, results can be produced at the radar site. It is possible for a single radar to track a satellite and produce results within 10 minutes after completion which can be a significant advantage under some circumstances. While experience has shown that results from a single track may be misleading, it may be possible to track several satellites in a fairly short period and the recovery of similar errors would tend to build confidence. This method has been used to provide a "quick look" at a radar after modification or major maintenance and later followed up with other methods.

The ability to run this type of software at the site can be a definite advantage. Care must be taken, however, to avoid misinterpretation of results. If results are interpreted at the site, someone with analytical ability should be available to review the data and reduce the chances of misinterpreting the results. Some examples of problems which could mislead even experienced analysts are shown in appendix B.

The major disadvantage is the ability to determine a given radar error model coefficient with accuracy and confidence. This method cannot be expected to produce the accuracy obtainable by using satellite ephemeris data.

### The Ephemeris Method

The method which makes use of the precise ephemeris data has significant advantages. These advantages are described below.

1. The standard for comparison is derived independent of radar data. The other methods depend on the radar data itself to estimate the position of the target.

2. The accuracy of the Doppler derived ephemeris data furnished by NSWC provides target position accuracy of 3- to 5-meters over the entire pass.

3. When compared with the BET method, the Ephemeris method is independent of analyst judgment. Radars cannot influence the estimated trajectory because of proper or improper weighting as selected by the analyst.

4. A single radar can be evaluated completely independent of any other radars. This factor alone is significant, but it is also important from a scheduling viewpoint, because it is usually more difficult to schedule several radars simultaneously for a BET.

5. The option exists to solve for several radar errors simultaneously without the additional burden of having to estimate the orbit. Droop, azimuth misalignment, azimuth bias, elevation bias, and others can be accurately estimated. In general, the coefficients can be more accurately estimated. In one example, the ephemeris was used to determine a site-location error. The use of ephemeris and the coherent transponders carried in the past have also provided an excellent means to measure range-rate bias errors and to evaluate phase-derived range systems at ranges where these exist.

6. Software is available to run on several mainframe computer systems and on the IBM-compatible PCs.

7. A satellite pass does not have to be selected with a geometry which satisfies multiple radars.

In the past, a major disadvantage was that the ephemeris data were not normally available for 5 to 7 working days, because the time was required to collect the Doppler data and then to process this data to the required trajectory accuracy. Currently, these data are available for the RADCAL satellite within 2-3 working days. Obviously a suitable satellite is required. Presently a calibration satellite (RADCAL) equipped with C-band radar transponders is available, but no such satellite was available for a 3-year period prior to the launch of RADCAL. Although there are currently several Navy navigation satellites equipped with Doppler transmitters, they are not equipped with C-band transponders. Because they are small and complex targets, the received signal levels are inadequate for use as calibration targets for all except high loop gain radars.

## Benefits Derived by Using Satellites

There is no other way to routinely monitor and detect some of the numerous calibration and performance problems which have been discovered by tracking the GEOS, GEOSAT, and RADCAL satellites. Without this type of monitoring, several of the problems identified and shown in appendix B would have been first observed during support of a live tracking operation, and the data distributed would have been adversely affected. Given the definition of radar performance maintenance that was provided earlier, it is hard to imagine another approach that could do the job or be as cost effective as tracking satellites. Experience of nearly 19 years using calibration satellites clearly supports this conclusion.

A major benefit of satellite tracking is that it provides a dynamic target traveling at high speed, and at an altitude which makes it possible for several radars to simultaneously track at rates similar to those experienced during ballistic missile or space launch operations. Using satellites, range-rate systems can be exercised over velocities ranging from plus to minus 22,000 feet per second. Since satellite passes are predictable well into the future, tracks can be planned weeks in advance with complete confidence that a target will appear near the expected time. In an emergency, passes may be scheduled the same day. Satellite pass track geometry can be selected to amplify the effects of errors or system problems which might be suspect.

When the satellite carries a C-band transponder and suitable antenna system, the satellite track data is collected in a benign tracking environment which helps to expose radar system problems. Many of these problems could be much more difficult to observe using skin-track mode with its attendant lower signal-to-noise ratio (SNR) and greater target dependency. Precise reference ephemerides provide a readily available "truth reference" with which to evaluate the track data.

Many of the radar problems identified via past satellite calibration efforts would have affected launch operation support if not discovered and corrected prior to launch. All would have had a serious degrading effect on user data, and some were significant enough to also adversely affect Range Safety Center data. Some examples are described next.

### Doppler Range-Rate Systems Acceleration Dependent Error

In 1975, within months after GEOS-C tracks were initiated, the cause of a major range-rate measurement problem was identified in MIPIR class radars. Resolution of this problem had been pursued by WTR and other government agencies for years. The first missile launch with a coherent transponder was in 1971 and this problem had precluded the use of range-rate data by post-flight data users. It appeared as a large unmodeled error proportional to range acceleration. On all missile launch operations, the error was disguised by target dependent flame effects during powered flight which is also, of course, the period of high range acceleration and range acceleration change.

The calibration satellite provided a target that could be tracked as often as four times a day. Although the total acceleration of the satellite is on the order of 30 ft/sec², the radar measurements in spherical coordinates (A, E, R and Rdot) can undergo very high accelerations and acceleration changes with the specific dynamics depending on the geometry of the pass. On a satellite pass, the range velocity is maximum while tracking it on the horizon as it moves more directly towards or away from the radar. Range acceleration is approximately zero at the horizon and is maximum at the point of closest approach (PCA). Since the Doppler-derived ephemeris data provided accurate position and velocity of the satellite, an excellent "truth reference" was available. In the relatively error free environment provided by transponder equipped satellite tracking, it was possible to confirm that the range-rate observation anomaly was indeed an acceleration dependent error. It was also noted that it was dependent on the radar Pulse Repetition Frequency (PRF) and that increasing the PRF decreased the effect of the error. The error was found to be repeatable and the problem turned out to be a design deficiency which was corrected by WTR at Vandenberg Air Force Base. The effect of the design problem was a timing error in the range-rate data caused by delays in the Doppler update track loop.

This problem was detected again several years later at the WTR's High Accuracy Instrumentation Radar (HAIR) after installation of the Doppler Velocity Extraction Subsystem (DVES). The manufacturer had not caught this problem in the design. The error was also discovered years later at another radar after depot level maintenance was completed. In each case it was easily identified by satellite tracking.

### Problems in the FPQ-6 RECS Upgrade

After the Radar Embedded Computer System (RECS) modification was made at the Pillar Point Air Force Station FPQ-6 radar, large angle trends were repeatedly observed in satellite track data. Using the variable geometry afforded by an orbiting satellite, passes were planned so as to have very high angular rates to amplify the effect of the problem. Numerous tracks showed this error to be repeatable. Repeatability is a key feature in solving many problems, and the satellite provides a target for repeatable testing. The problem, which was eventually found to be a time tag error unique to the angle data, was caused by a wiring problem.

### The Nth Time Around Range Problem at Kokee Park

A range measurement problem, characterized by increased noise and trending, appeared in Minuteman reentry vehicle (RV) track data collected by the Kokee Park FPS-16 radar. At distances in the vicinity of 512 and 1024 miles, large errors in observed range were noted. Several satellite tracks were used to confirm that the problem was related to the Nth time around subsystem within the range machine. When working correctly, the Nth time around system permits the radar to track through regions where returns from the target coincide with the normal time for subsequent transmitter firings. The error was initially observed on a launch operation through a BET analysis. Since this error was visible in satellite track data, several tracks were scheduled to troubleshoot and eliminate the problem and confirm the fix. This error could only be observed in digital data, and there was no other available method to reproduce it.

### A Doppler System Problem at the MPS-36

A large error in measured range-rate was observed at the Pillar Point Air Force Station MPS-36 radar when the range-rate was greater than 16,000 feet per second. Because of this range-rate, the error was only observable in ballistic missile track and satellite track data. This error has reoccurred on two occasions some years apart. It is clearly observable in satellite track data and detectable as part of a routine maintenance program using satellites. The system anomaly, if not detected and eliminated, would have resulted in unusable data being recorded during a missile tracking operation. Aircraft could not be used to locate this error, since they cannot achieve the necessary velocities for problem detection.

### Data Time Tag Error Detection

Timing errors of 9 milliseconds at Tonopah Test Range and 3 milliseconds at Edwards Air Force Base radars were detected by the satellite and the associated ephemeris data. These sites used Cesium clocks for timing, but the errors resulted from the method employed to record data on tape. These errors, while easily detected with a highly dynamic target, were not detected in the data collected on the targets normally tracked by these radars.

## Other Advantages Offered by Satellite Tracking

Engineering and maintenance certification is much easier with the satellite. It is possible to install major modifications in radar systems, track several satellite passes, and certify the radar as operational. Several radar problems have been discovered after system modifications in satellite track data. Problems have also been found after depot-level maintenance and other maintenance programs.

Satellites with their coherent C-band transponders provide the only means to test radar hardware and software modifications in a dynamic environment similar to that in which the radar is to be used. With any such satellite, there are suitable passes available several times each day to provide tracking opportunities and, consequently, to provide assurance that the radars will be ready to support a launch operation. A satellite such as GEOSAT has provided a maintenance tool unmatched by anything else for monitoring radar performance. It has provided the tool to identify and to correct several major problems with minimal impact on operational support and has proven invaluable to engineering elements in their radar engineering efforts.

Cost savings is significant when compared to other methods previously used at some of the ranges. For example, at WTR, radars track a satellite for 15 minutes instead of the several hours previously required for tracking an instrumented (expensive to operate) aircraft. Additionally, a greater number of errors can be measured. Tracks can be accomplished at predictable times, usually during the day instead of at night, to reduce overtime. Unlike the aircraft, the satellite never cancels and never holds. Data processing time, which consumed many man-hours and a relatively large amount of computer time, was reduced to minutes for setup and less than 1 minute to run on a personal computer.

## Practical Considerations for Radar Calibration

### Scheduling and Pass Selection

Even though a satellite may be in an orbit suitable for radar calibration, passes must be selected which provide the best opportunity to measure the errors of interest. Errors easily measured by tracking satellites are azimuth bias, elevation bias, range bias, range-rate bias, azimuth RF misalignment (azimuth skew), and droop. Dynamic lag may also be evaluated. Errors such as axis nonorthogonality, pedestal mislevel, and encoder nonlinearity are best measured by other means. Consideration must be given to the errors to be measured prior to selecting a satellite pass for radar calibration.

While any pass may be used for estimating range bias, this is not the case for some of the angular errors. Antenna droop and azimuth misalignment are examples of errors where the magnitude varies as a function of the elevation angle. The droop error looks very much like elevation bias if a pass with a maximum elevation angle of only 15° is tracked. The droop error is a function of the cosine of elevation and the difference between the cosine of 0 and 15° is negligible. Azimuth misalignment is a function of the secant of elevation which also changes little unless elevation is changed sufficiently. On the other hand, a pass where the radar tracks from the horizon to an elevation angle of 80° may be used to provide good estimates of these errors.

The Normal/Plunge scenario should be considered for tracking the high elevation passes. Plunge refers to tracking with the antenna between 90 and 180° in elevation. In this scenario, the satellite is acquired in the normal position at or near the horizon. Track is subsequently dropped just before (or after) PCA and the target is reacquired in the plunge mode for tracking to the horizon. This type of track is very useful for separating the azimuth bias from the azimuth misalignment error, because, unlike the bias, the sign of the misalignment error will change between normal and plunge. This mode also extends elevation track beyond 90° for evaluation of droop symmetry.

Pass selection is made by using the NORAD two line element set and prediction software to provide time at the horizon and time at PCA for a desired satellite. Azimuth, elevation, and range are also given for these times, so suitable passes may be selected for tracking. An example of a two line element set for object 22698 (RADCAL satellite) is provided below.

### NORAD 2 LINE ELEMENT SET

```
1 22698U 93041A   94192.83735015  .00000041  00000-0  11713-4 0  3122
2 22698  89.5478 308.1313 0093279 106.1395 255.0087 14.21315027 54095
```

### Preliminary Pass Predictions

An example of information produced by using the element set with the LOOKS program appears on the following page. This information, showing predictions for three radar sites for a 4-day period, would be used for planning and scheduling of radar tracks. The prediction only shows information for PCA. Suitable calibration passes could be selected from this list.

# Predicted Pass PCA Time for Object #22698

[TABLE PLACEHOLDER: Pass predictions for multiple sites over 4-day period showing Site, Year, Day, PCA time, Start/Stop times, Length, Elevation, Azimuth, Range, and Revolution number]

Example entries:
- Mugu: Day 288, PCA 04:02:41, El 13.30°, Az 278.94°, Rng 2465.07 km
- TPQ-1: Day 288, PCA 04:02:47, El 15.45°, Az 278.16°, Rng 2317.15 km
- MPS-3: Day 288, PCA 04:03:33, El 19.21°, Az 277.84°, Rng 2087.96 km

This example indicates that RADCAL is viewable during four different periods on day 286. Each line provides PCA time with azimuth, elevation, and range points. Since data are supplied only for PCA, the elevation column displays the maximum elevation during the pass. Although any pass may be used as a general check of the radar, only the higher elevation passes would be used to evaluate the azimuth misalignment or droop errors. Consequently, the two passes with low elevation angles at PCA would not normally be selected for tracking. The second pass on day 286 (Rev 6734) provides good pass geometry, and the program is used to expand information for the MPS-36 radar as presented next. The first and third lines show horizon time. Information at PCA appears on the second line.

This information would be passed to the radar site for scheduling purposes.

## Expanded Pass Information

[TABLE PLACEHOLDER: Detailed pass information for MPS-36 showing Year, Day, Time, Elevation, Azimuth, Range, Edot, Adot, and Rdot at horizon and PCA times]

If the radar site does not have software for automatic acquisition, the program may be used to produce look angles at selected intervals for manual acquisition. An example of such an output with 30 second intervals selected is shown below.

## Radar Look Angles for Object #22698

[TABLE PLACEHOLDER: MPS-36 look angles at 30-second intervals showing Time, Elevation, Azimuth, Range, Edot, Adot, and Rdot from acquisition through loss of signal]

### Tracking Considerations

The reasons for tracking satellites are numerous, and so are the considerations for setup and operation of the radar. Setup may vary depending on test requirements. For the purpose of routine radar calibration and performance monitoring, consistency is very important. It dictates that system preoperational calibrations be accomplished in accordance with a procedure, and that operating parameters such as servo bandwidth and pulse width be consistent from pass to pass. If radars of the same or similar type, will be compared, it is also important that tracking parameters be the same at all radars. Radar data can certainly be improved by correcting for known errors provided the pass-to-pass variability is low. Consistency during operation and setup of the radar is necessary to reduce variability of the estimated errors to a minimum. 

The following chart shows estimates of azimuth misalignment, elevation bias, range bias, range-rate bias, and droop for a 3-month period at a MIPIR radar. The RADCAL satellite was used to estimate the errors. Note that although the azimuth misalignment error at this radar is large (-0.16 mils), the standard deviation is low (0.02 mil). Therefore, the azimuth misalignment error at this radar can be corrected for in post-mission processing with confidence since the estimate for this error is consistent from one tracking operation to the next. The standard deviation for the range bias estimate (3 feet) would not be this small if the radar operators had not properly calibrated the radar prior to tracking. Once established, any significant increase in the standard deviation would normally be cause to suspect a problem with the radar.

## Quarterly Statistics for TPQ-18 Radar

[TABLE PLACEHOLDER: Statistical data showing DATE, REV/OPT, AMIS, EBIAS, RBIAS, RDOT, DROOP, AZERO, and various SIG values for multiple tracking sessions from July through September 1994]

### Considerations During Analysis

This document is not intended to present details concerning the analysis of satellite tracking data; however, some precautions are in order concerning the use of a priori corrections. If a program such as RPM is used, it is easy to produce incorrect estimates for some of the errors. For example, if the azimuth bias is significant and RPM is used to estimate azimuth RF misalignment during a normal only (no plunge) pass, an error in the estimate will result. The azimuth bias should be known and used as an input to the program prior to execution.

The actual bias can be determined by star observations (recommended method) or by solving for both the misalignment and the bias using the normal/plunge tracking mode. Errors in the estimate of azimuth misalignment will also occur if the axis nonorthogonality error is not known or corrected during program execution. In one case, the error is a function of the tangent of the elevation angle, and in the other, it is a function of the secant of elevation.

The following graphs of the Multiple Object Tracking Radar (MOTR) azimuth residuals illustrate the problem. 

- **Figure 1** shows residual errors when the program does not solve for or correct for any parameters affecting azimuth. It is the equivalent of comparing the MOTR azimuth data with the reference ephemeris for the satellite, where all errors appear in the plot.

- **Figure 2**: The program is allowed to solve for and correct for azimuth bias, azimuth misalignment (skew), and axis nonorthogonality. The corrections applied are +0.31 mil for azimuth misalignment, -0.26 mil for azimuth bias, and +0.04 mil for nonorthogonality and, except for the random errors, the residual errors are small. Note that the solution for azimuth misalignment and azimuth bias are almost equal in magnitude and opposite in sign.

- **Figure 3** shows results when the program solves for azimuth misalignment and azimuth bias. Estimates of the azimuth misalignment term is +0.25 mil and the bias estimate is -0.22 mil.

- **Figure 4**: The program is allowed to solve for azimuth misalignment only. A value of 0.10 is estimated and residual errors are much greater.

- **Figure 5** shows results when solving for bias and nonorthogonality. Bias is estimated at -0.03 mil and nonorthogonality is +0.19 mil, producing low residuals as shown in the graph.

The results indicate that nonorthogonality and azimuth misalignment are highly correlated. In addition, solving for RF misalignment without using an a priori correction for bias can produce misleading results. Nonorthogonality and azimuth bias can be measured independently and a priori corrections can be applied in the program to better estimate the other terms.

[FIGURES 1-5 PLACEHOLDER: Series of azimuth residual plots for MOTR Rev 07024/T1202/Ephemeris showing different correction scenarios]

Several graphical examples of radar errors detected as a result of tracking satellites are presented in appendix B. These examples clearly show the requirements for radar performance monitoring if quality data is a requirement. While some of the examples in appendix B were furnished by other ranges, the majority were produced by the Air Force 30th Space Wing formerly referred to in this document as the Air Force Western Test Range.

---

## APPENDIX A: SINGLE REVOLUTION ORACLE ACCURACY

A comparison of results to determine the accuracy of the two-pass ORACLE software, now referred to as ORCA, was made in 1980. Although not shown here, these results were not significantly better than those obtained from the program after it was modified to work with a single pass.

Single-pass ORACLE results were compared with RPM (using ephemeris data processed by NSWC) in 1989 and more extensively in 1990. Some examples from the 1990 ORACLE comparison are presented and explained here. Results for all radars used in this test are included. These important points should be kept in mind.

1. The ephemeris data are considered to be the standard for determining radar errors. Thus the errors derived from RPM software using the ephemeris data were considered to be the standard by which the ORACLE results were judged.

2. The GEOSAT satellite was used for all tests. The signal was from a point source (antenna) and was supplied by a 100-watt transponder. Signal level at the radars was above 20 dB signal-to-noise ratio with no fading during the pass.

3. Although the results from ORACLE may look very good for some measured parameters, it has definitely been determined that stability is much poorer for skin-tracked targets. This stability was immediately evident after the loss of GEOSAT when the skin mode was used for tracking other satellites. It is obvious that good data is essential for building a high quality reference orbit.

An example of how results were compared for each radar is at table A-1. The table on the left shows radar errors estimated for the HAIR radar (033001) using the RPM software. The Naval Surface Warfare Center (NSWC) supplied the ephemeris data derived from Doppler data from the GEOSAT satellite. The first column contains the revolution number of the GEOSAT satellite tracked by the radar. The second column shows the estimate of the azimuth misalignment (AMIS), and the third column notes the elevation bias errors (EBIAS) (expressed in mils). The range bias (in feet), azimuth zero set error, and the antenna droop (expressed in mils) appear in the fourth through sixth columns. Run sigmas (SIGA, SIGE, and SIGR) in the last three columns are indicative of random errors or trends in the data. The mean and standard deviation at the bottom of the RPM table represent the mean of the nine passes and the variability for these passes.

Results using the ORACLE software are in the middle table.

The table on the right shows the differences between the errors as estimated by the two techniques. The mean value in this table provides the mean of the differences for each parameter. The standard deviation provides an indication of the variability of these differences. Results indicate that ORACLE does a fair job of estimating azimuth misalignment, elevation bias, and droop.

While the mean for range bias is only -9 feet, the standard deviation of 35 feet points out that the range bias estimates are inconsistent. In the case of azimuth encoder bias (AZERO), the estimate is consistently poor with a mean difference of -0.32 mils and a standard deviation of 0.08 mils.

[TABLE A-1 PLACEHOLDER: Oracle/RPM Comparison for Hair Radar showing three tables - RPM results, ORACLE results, and their differences]

Information in the third table is also included as part of table A-2, along with results from several other radars. The mean and standard deviation (1 sigma) values at the bottom of table A-2 provide an excellent comparison with RPM for elevation bias and droop, a fair comparison for azimuth misalignment and a poor comparison for range and azimuth biases. Data for other radars which appear in table A-2 are included in tables A-3 through A-7.

[TABLE A-2 PLACEHOLDER: Oracle/RPM Differences summary for all radars]

[TABLES A-3 through A-7 PLACEHOLDER: Detailed comparison tables for FPS-16 #1, FPS-16 #2, FPQ-6, MPS-36, and FPQ-14 radars]

Significantly more data was collected for this study. Only that data collected where the radar tracked in the Normal/Plunge mode is included here. In collecting data in this fashion, the radar operator tracks the first half of the pass in normal mode, then drops track at the point of closest approach (PCA) and switches to plunge mode for the remainder of the pass. This mode is used when the maximum anticipated elevation angle during the pass exceeds 65°. (NOTE: The normal/plunge mode refers to the position of the antenna. The antenna is between 0 and 90° elevation in the normal mode and between 90 and 180° in the plunge mode.) Radar operators are requested to track in the normal mode if the maximum expected elevation angle is less than 65°. Passes are not selected for calibration tracks unless the elevation angle is expected to reach 45° or more at PCA. Estimates for azimuth misalignment and azimuth bias are improved by tracking in the normal/plunge mode.

Results for the normal only tracks are not included, because the ORACLE results were significantly poorer as compared to RPM. If ORACLE is used, it is highly recommended that track data be collected in the normal/plunge for best results.

The ORACLE has been known to estimate errors which are unreasonable as evident in the tables included here for azimuth bias. The program is known to assign errors to incorrect areas. For example, in appendix B (figures B-17 and B-17A) an error, known to exist in range, was plotted as an error in range rate. The range error in this case went undetected by ORACLE.

---

## APPENDIX B: RADAR SYSTEMS ERRORS DETECTED BY TRACKING SATELLITES

This appendix describes errors detected as a result of tracking satellites. While much of the information presented here is based on the experience at the Air Force Western Test Range (WTR), operated by the 30th Space Wing, some information was made available from other test ranges. While the number of errors presented here are small, compared to those detected, enough information is provided to show the benefits derived by tracking a calibration satellite.

### Description of RPM Plots

A detailed description of the first four graphs, produced by the RPM software, provides an introduction to better understand the graphical information which follows. The graphs show data which should be expected for a radar which is operating normally.

#### Normal Range Data from FPQ-6

Figure B-1 shows RPM range tracking results from the FPQ-6 radar. The noise level is low and trends are not evident. (The majority of the samples are within plus and minus 2 feet.) This is an example of a radar operating normally. Time, on the X axis, is in seconds. Zero on this scale represents the starting time as selected by the analyst. This time could be horizon time, but it usually coincides with the time the radar reaches 15° in elevation. The range error, on the Y axis, is scaled in feet. The standard used to determine range error is the precise ephemeris data derived from the Doppler tracking network. Radar data versus ephemeris is plotted at 2 samples per second in this example. The radar data is unfiltered. While some points may be edited, the data is not smoothed.

Since the plot is compressed to cover a page, several points are plotted in a column. The asterisk is used as a plotting symbol prior to point of closest approach (PCA) and the plus sign is used after this point. The letter "P" is used to replace one of these symbols if the radar is tracking in the plunge mode. An "E" indicates that the data point was edited for purposes of estimating the radar errors, but it is not edited from the plot. Any range bias is removed before plotting. This bias is listed by the program and used by the analyst in evaluating the radar. Azimuth, elevation, and range appear at the bottom of the page for Acquisition of Signal (AOS), PCA, and Loss of Signal (LOS) times to provide information concerning pass geometry. Deviation from the center (zero error) in this example is almost entirely because of noise or random errors.

[FIGURE B-1 PLACEHOLDER: Range differences plot for FPQ-6 showing normal operation]

#### Normal Azimuth Data for FPQ-6

Azimuth data from the same radar is displayed in figure B-2. For angles, the Y axis scaling is in mils. With this exception, the comments concerning the plot in the above paragraph applies here. This is an example of a well behaved radar with low angle noise level and no trends evident in the plot.

[FIGURE B-2 PLACEHOLDER: Azimuth differences plot for FPQ-6 showing normal operation]

#### Normal Elevation Data for FPQ-6

Elevation data from the same radar are shown in figure B-3. Noise content is low with no noticeable trends.

[FIGURE B-3 PLACEHOLDER: Elevation differences plot for FPQ-6 showing normal operation]

#### Normal Range Rate Data for FPQ-6

Figure B-4 is used to illustrate data from the same radar. This is an example of radial velocity data derived from one of the many coherent radars used at the WTR. Range rate, also referred to as Rdot, errors are in feet per second.

This graph does indicate a problem. Random errors are almost twice as great as they should be as compared with other range rate systems used at the WTR.

[FIGURE B-4 PLACEHOLDER: Range rate differences plot for FPQ-6 showing elevated noise]

### Examples of Specific Radar Errors

#### Azimuth Misalignment Error (FPS-16)

An example of azimuth misalignment at an FPS-16 radar is displayed in figure B-5. In this case the RF feed was realigned to correct the error. Note that this error becomes very large at higher elevation angles (refer to 286 seconds). Therefore, it is easily detected in satellite track data provided the analysis software used is capable of solving for azimuth misalignment and not just azimuth bias. The RPM solves for both. The radar initially tracked in plunge and switched to normal near PCA. The magnitude of the error was 0.42 mils. The sign of the error changes when in the plunge mode. Figure B-5A shows the data after the correction for 0.42 mils was made. A dynamic lag error (caused by acceleration) was masked in figure B-5. This error was revealed after the azimuth misalignment error was removed. It is clearly evident in figure B-5A.

[FIGURES B-5 and B-5A PLACEHOLDER: Azimuth misalignment error plots before and after correction]

#### Droop Error at FPQ-6

Figure B-6 shows a large antenna droop error which came as a surprise after an upgrade to the RF feed was made at this MIPIR (FPQ-6) radar. Prior to this time, droop was consistent and very small. Similar results were noted at all other radars where this modification was subsequently installed. The magnitude of this error varies between -0.29 mil at the horizon to 0 at 90° elevation. Since the second part of the track was made in plunge, the error continues to increase after PCA. In a normal track, the error would have decreased after PCA to -0.29 mil.

Figure B-6A shows the elevation data after correction for the error estimated by the RPM software was applied. This error is present in all MIPIR, FPS-16, and MPS-36 radars.

[FIGURES B-6 and B-6A PLACEHOLDER: Droop error plots before and after correction]

#### Velocity Sensitive Range Rate Error (MPS-36)

The error presented in figure B-7 was observed several times prior to being corrected. This is range-rate data from an MPS-36 radar located at Pillar Point Air Force Station. Data are usable only when velocity is within ±16,000 feet per second and totally unusable outside of this range. After correction, this problem reoccurred more than 1 year later. This problem could only be observed while tracking satellites and on launch operations from Vandenberg Air Force Base.

[FIGURE B-7 PLACEHOLDER: Velocity sensitive range rate error plot]

#### Doppler Design Error (HAIR)

The error in figure B-8 was detected after the Digital Velocity Extraction System (DVES) was installed at the Vandenberg Air Force Base HAIR. It was the result of a design error. This type of problem appeared in the original range rate system referred to as the Coherent Signal Processor (CSP). Unless it is corrected, the data is unusable. The CSP was unusable for years until the error was identified through satellite tracking.

[FIGURE B-8 PLACEHOLDER: Doppler design error plot]

#### Angle System Oscillation (MPS-36)

Oscillatory problems in the angle system at a MPS-36 radar are shown in figures B-9 (azimuth) and B-9A (elevation). Problems were corrected and verified by a subsequent pass of the GEOS satellite.

[FIGURES B-9 and B-9A PLACEHOLDER: Angle system oscillation plots for azimuth and elevation]

#### Intermittent Azimuth Bits (TPQ-18)

An intermittent condition affecting azimuth data at the Vandenberg Air Force Base TPQ-18 radar appears in figures B-10, B-10A, and B-10B. Two sets of data, spaced approximately 0.2 mils apart, are shown here. It was believed that this problem, caused by a missing bit (0.195 mil) had been eliminated, but it appeared 17 days later (see figure B-10A). After being noted a third time (see figure B-10B), some 2 months later, the problem was finally fixed by changing the azimuth encoder.

[FIGURES B-10, B-10A, B-10B PLACEHOLDER: Intermittent azimuth bits plots]

#### Digital System Error (FPS-16, HAIR, TPQ-18 Radars)

Digital data problems have been detected on numerous occasions. Figure B-11 shows a missing bit at a Vandenberg FPS-16 radar. The bit represents 11.25° in elevation. When the bit should be present in the digital data, elevation appears to be 11.25° lower than it really is, although it does not appear on this plot because of the scale used. Figure B-11A shows a digital problem at the HAIR. In this case the 0.39 mil bit is missing. Figure B-11B shows the 7.81 yard bit to be missing at the Vandenberg TPQ-18 radar.

[FIGURES B-11, B-11A, B-11B PLACEHOLDER: Digital system error plots for various radars]

#### Range Error Caused by Tuning (Kokee Park FPS-16)

All errors are not caused by equipment. Figure B-12 shows a range error caused by tuning while tracking at the Kokee Park FPS-16 radar. Site procedures were changed after observing this problem at other radars. Through routine satellite tracking operations, radar operators have become aware of the effects caused by their actions. Examples like these are rarely seen at the WTR radars today.

[FIGURE B-12 PLACEHOLDER: Range error caused by tuning]

[Additional figures B-13 through B-23A continue with similar format describing various radar errors and problems]

### Examples of Errors from a Historical Data Base

Many of the problems experienced when using satellites are not graphed. They were found by observing changes from nominal. The following list was compiled by extracting information from a series of historical monthly reports covering a 3-year period (1982 to 1985). During this time period, the ephemeris data, used as the standard to compare the radar data was often unavailable for 30 to 40 days. By the time errors were detected, launch data was often affected. To ensure quality radar data, tracking must be accomplished often and ephemeris data must be available within a few days.

**Selected Historical Examples:**

- **January 1982**: Significant increase in range bias from radar 023001 and 023002.
- **March 1982**: Large (-0.9 mil) bias seen in FPS-16 #2 satellite tracking operation was believed to be caused by defective waveguide switch. Repaired waveguide shutter and eliminated problem.
- **May 1982**: Large misalignment (-0.49 mil) with Non Coho beacon tracking conditions. Error varies with frequency.
- **June 1982**: 100 mil azimuth and elevation error at the TPQ-18.
- **July 1982**: Excessive angle bias variability for FPS-16 #2 caused by problem with defective RF feed retaining hardware (broken feed horn bracket). Repairs made.
- **August 1982**: ±5.0 mil azimuth trend FPS-16 #1; ±1.5 mil azimuth trend FPS-16 #2
- **September 1982**: Large angle oscillations, peak amplitude exceeded 1 mil at MPS-36; Elevation bias variability excessive for FPQ-14; A 1 hour, 8 minute timing jump identified at TPQ-18.
- **October 1982**: Three of five satellite tracks show 192,000 foot range bit as intermittent at TPQ-18.

[Continues with additional historical examples through 1985-1986...]

### Summary

While the above list covers a small period, it provides several examples to show problems discovered as a result of tracking satellites. Many of these problems would have degraded data from launch operations if not detected and eliminated.