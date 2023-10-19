/*
##### Data Cleaning:
## Remove Mr.,Mrs.,Ms.,Dr. from name

select name , replace(name,substring(name, 0, CHARINDEX('.',left(name,4))+1), '')
from dbo.patient_df

update dbo.patient_df
set name = replace(name,substring(name, 0, CHARINDEX('.',left(name,4))+1), '')

update dbo.patient_df
set name = TRIM(name)

select * from dbo.patient_df
*/


drop table if exists #Temp_tab1
-- Create a temp table, whenever the condition satisfies assign 1 to corresponsing column else 0
select patient_id, response_value, Curr_Const,past_const,med_const, not_med_const
into #Temp_tab1
from (
		select patient_id,
			response_value,
			(case when (data_category = 'current_conditions' 
			and lower(response_value) like '%constipation%') Then 1 
			else 0 
			end) as Curr_Const,

			(case when (data_category = 'past_conditions' 
				and (upper(response_value) like '%IBSC%' 
					OR UPPER(response_value) like '%IBS-C%'
					OR lower(response_value) like '%irritable%syndrome%constipation%'
					OR lower(response_value) like '%chronic%idiopathic%'
					OR lower(response_value) like '%idiopathic%constipation%'
					OR lower(response_value) like '%chronic%idiopathic%constipation%'
					OR upper(response_value) like '%CIC%')) THEN 1 
			else 0 
			end) as past_const,

			(case when (data_category ='medications' 
				and (lower(response_value) like '%amitiza%'
					OR lower(response_value) like '%cephulac%'
					OR lower(response_value) like '%chronulac%'))THEN 1 
			else 0 
			end) as med_const,

			(case when (data_category = 'medications'
				and(lower(response_value) like '%lubiprostone%'
					OR lower(response_value) like '%osmoprep%'
					OR lower(response_value) like '%plecanatide%'
					OR lower(response_value) like '%trulance%')) THEN 1 
			else 0 
			end) as not_med_const
		from  dbo.response_df
	) as output1

-- Select patient_id and corresponsing columns based on the sum of rows count for Curr_Const,past_const,med_const, not_med_const grouped by patients


--select count(distinct patient_id)
--from (
select t.patient_id,
		substring(p.name, 0, CHARINDEX(' ',p.name)) as 'Patient First Name',
		SUBSTRING(p.name,CHARINDEX(' ',p.name), len(p.name)) as 'Patient Last Name',
		DATEDIFF(Year,p.birthdate,GETDATE()) as 'Patient Age',
		p.sex as 'Patient Sex',
		left(right(p.address,8),2) as 'Address State',
		r.response_value
from #Temp_tab1 as t
inner join 
dbo.patient_df as p
on t.patient_id = p.patient_id
left join 
dbo.response_df as r
on t.patient_id = r.patient_id
group by t.patient_id, p.name,p.birthdate,p.sex,p.address,r.response_value
having ((
		sum(Curr_Const) > 0 
		OR 
		(
			sum(past_const) >0 
			and 
			sum(med_const) >0 
		)
		)
		and sum(not_med_const) = 0)

--) as a

