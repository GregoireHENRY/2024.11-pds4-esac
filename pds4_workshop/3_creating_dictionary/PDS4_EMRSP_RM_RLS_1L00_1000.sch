<?xml version="1.0" encoding="UTF-8"?>
  <!-- PDS4 Schematron for Name Space Id:emrsp_rm_rls  Version:1.0.0.0 - Thu Nov 07 11:46:26 CET 2024 -->
  <!-- Generated from the PDS4 Information Model Version 1.21.0.0 - System Build 14.0 -->
  <!-- *** This PDS4 schematron file is an operational deliverable. *** -->
<sch:schema xmlns:sch="http://purl.oclc.org/dsdl/schematron" queryBinding="xslt2">

  <sch:title>Schematron using XPath 2.0</sch:title>

  <sch:ns uri="http://www.w3.org/2001/XMLSchema-instance" prefix="xsi"/>
  <sch:ns uri="http://pds.nasa.gov/pds4/pds/v1" prefix="pds"/>
  <sch:ns uri="https://psa.esa.int/psa/emrsp/rm/rls/v1" prefix="emrsp_rm_rls"/>

		   <!-- ================================================ -->
		   <!-- NOTE:  There are two types of schematron rules.  -->
		   <!--        One type includes rules written for       -->
		   <!--        specific situations. The other type are   -->
		   <!--        generated to validate enumerated value    -->
		   <!--        lists. These two types of rules have been -->
		   <!--        merged together in the rules below.       -->
		   <!-- ================================================ -->
  <sch:pattern>
    <sch:rule context="emrsp_rm_rls:Autofocus_Data/emrsp_rm_rls:criticality">
      <sch:assert test=". = ('02', '03')">
        <title>emrsp_rm_rls:Autofocus_Data/emrsp_rm_rls:criticality/emrsp_rm_rls:criticality</title>
        The attribute emrsp_rm_rls:Autofocus_Data/emrsp_rm_rls:criticality must be equal to one of the following values '02', '03'.</sch:assert>
    </sch:rule>
  </sch:pattern>
  <sch:pattern>
    <sch:rule context="emrsp_rm_rls:Autofocus_Data/emrsp_rm_rls:end_of_test_trigger">
      <sch:assert test=". = ('0', '1')">
        <title>emrsp_rm_rls:Autofocus_Data/emrsp_rm_rls:end_of_test_trigger/emrsp_rm_rls:end_of_test_trigger</title>
        The attribute emrsp_rm_rls:Autofocus_Data/emrsp_rm_rls:end_of_test_trigger must be equal to one of the following values '0', '1'.</sch:assert>
    </sch:rule>
  </sch:pattern>
  <sch:pattern>
    <sch:rule context="emrsp_rm_rls:Autofocus_Data/emrsp_rm_rls:laser_channel">
      <sch:assert test=". = ('0', '1')">
        <title>emrsp_rm_rls:Autofocus_Data/emrsp_rm_rls:laser_channel/emrsp_rm_rls:laser_channel</title>
        The attribute emrsp_rm_rls:Autofocus_Data/emrsp_rm_rls:laser_channel must be equal to one of the following values '0', '1'.</sch:assert>
    </sch:rule>
  </sch:pattern>
  <sch:pattern>
    <sch:rule context="emrsp_rm_rls:Autofocus_Data/emrsp_rm_rls:preamplifier_gain">
      <sch:assert test=". = ('0', '1', '2', '3')">
        <title>emrsp_rm_rls:Autofocus_Data/emrsp_rm_rls:preamplifier_gain/emrsp_rm_rls:preamplifier_gain</title>
        The attribute emrsp_rm_rls:Autofocus_Data/emrsp_rm_rls:preamplifier_gain must be equal to one of the following values '0', '1', '2', '3'.</sch:assert>
    </sch:rule>
  </sch:pattern>
  <sch:pattern>
    <sch:rule context="emrsp_rm_rls:Autofocus_Data/emrsp_rm_rls:step_mode">
      <sch:assert test=". = ('0', '1', '2')">
        <title>emrsp_rm_rls:Autofocus_Data/emrsp_rm_rls:step_mode/emrsp_rm_rls:step_mode</title>
        The attribute emrsp_rm_rls:Autofocus_Data/emrsp_rm_rls:step_mode must be equal to one of the following values '0', '1', '2'.</sch:assert>
    </sch:rule>
  </sch:pattern>
  <sch:pattern>
    <sch:rule context="emrsp_rm_rls:Instrument_Status/emrsp_rm_rls:criticality">
      <sch:assert test=". = ('02', '03')">
        <title>emrsp_rm_rls:Instrument_Status/emrsp_rm_rls:criticality/emrsp_rm_rls:criticality</title>
        The attribute emrsp_rm_rls:Instrument_Status/emrsp_rm_rls:criticality must be equal to one of the following values '02', '03'.</sch:assert>
    </sch:rule>
  </sch:pattern>
  <sch:pattern>
    <sch:rule context="emrsp_rm_rls:Instrument_Status/emrsp_rm_rls:instrument_status_type">
      <sch:assert test=". = ('1', '2', '4')">
        <title>emrsp_rm_rls:Instrument_Status/emrsp_rm_rls:instrument_status_type/emrsp_rm_rls:instrument_status_type</title>
        The attribute emrsp_rm_rls:Instrument_Status/emrsp_rm_rls:instrument_status_type must be equal to one of the following values '1', '2', '4'.</sch:assert>
    </sch:rule>
  </sch:pattern>
</sch:schema>
