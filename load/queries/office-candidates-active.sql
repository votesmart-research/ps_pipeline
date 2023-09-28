/*
Author: Johanan Tai
Description: Queries office candidates (incumbents) by the start to the end of their terms
*/


SELECT
	DISTINCT
    candidate.candidate_id,
    concat_ws(' ',
			  candidate.firstname, 
			  concat('"',candidate.nickname, '"'),
			  candidate.lastname
			 ) as "candidate_name",
    office.name AS office,
    state.name AS state,
    state.state_id AS state_id,
    districtname.name AS district,
    party.name AS party

FROM office_candidate
JOIN candidate USING (candidate_id)
JOIN officecandidatestatus USING (officecandidatestatus_id)

LEFT JOIN office USING (office_id)
LEFT JOIN state ON office_candidate.state_id = state.state_id
LEFT JOIN districtname USING (districtname_id)
LEFT JOIN office_candidate_party USING (office_candidate_id)
LEFT JOIN party ON office_candidate_party.party_id = party.party_id


WHERE   
	office.office_id IN (1,5,6)
	AND
	officecandidatestatus.name = 'active'