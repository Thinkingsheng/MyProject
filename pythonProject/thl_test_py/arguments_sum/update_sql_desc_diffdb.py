# -*- coding:utf-8 -*-

datavm_data = {
    # 此参数需调用global_fun.get_start_date函数获取开始日期
    'start_date_sql': """
    SELECT max(`day`) as `day` FROM dm_yingyun_zhengjia_flow_arrive_day
    """,
    # 输出的目标表
    'append_table': 'dm_yingyun_zhengjia_flow_arrive_day',
    # 要替换 ${b_date} 参数
    'data_sql': """
SELECT
	b_date as `day`,
	num as `number`

FROM
(
	select
		(case
			when (c.daily_custom_num_type = 2
			and u.m_num > 0) then u.m_b_date
			else u.d_b_date
		end) as b_date,
		(case
			when (c.daily_custom_num_type = 2
			and u.m_num > 0) then u.m_mall_id
			else u.d_mall_id
		end) as mall_id,
		MAX((case
			when (c.daily_custom_num_type = 2
			and u.m_num > 0) then u.m_num
			else u.d_num
		end)) as num,
		(case
			when (c.daily_custom_num_type = 2
			and u.m_num > 0) then u.m_data_time
			else u.d_data_time
		end) as data_time
	from
		(
			(
			select
				ml.b_date as m_b_date
				,ml.mall_id as m_mall_id
				,ml.num as m_num
				,ml.data_time as m_data_time
				,ml.supplier as m_supplier
				,dl.b_date as d_b_date
				,dl.mall_id as d_mall_id
				,dl.num as d_num
				,dl.data_time as d_data_time
				,dl.supplier as d_supplier
			from
				`datavm`.`cf_face_cust_in_num_statistics_all_device_history` ml
				left join `datavm`.`cf_face_cust_in_num_statistics_door_level_history` dl 
				  on dl.b_date = ml.b_date
				  and dl.mall_id = ml.mall_id
				  and dl.supplier = ml.supplier
			)
		union
			(
			select
				ml.b_date as m_b_date
				,ml.mall_id as m_mall_id
				,ml.num as m_num
				,ml.data_time as m_data_time
				,ml.supplier as m_supplier
				,dl.b_date as d_b_date
				,dl.mall_id as d_mall_id
				,dl.num as d_num
				,dl.data_time as d_data_time
				,dl.supplier as d_supplier
			from
				`datavm`.`cf_face_cust_in_num_statistics_door_level_history` dl 
				left join `datavm`.`cf_face_cust_in_num_statistics_all_device_history` ml
				  on dl.b_date = ml.b_date
				  and dl.mall_id = ml.mall_id
				  and dl.supplier = ml.supplier
			)
		) u
		left join `datavm`.system_data_config_history c on IFNULL(u.m_mall_id,u.d_mall_id) = c.mall_id and IFNULL(u.m_b_date,u.d_b_date) = c.b_date
		
	GROUP BY
			(case
			when (c.daily_custom_num_type = 2
			and u.m_num > 0) then u.m_b_date
			else u.d_b_date
		end),(case
			when (c.daily_custom_num_type = 2
			and u.m_num > 0) then u.m_mall_id
			else u.d_mall_id
		end)
) t1
WHERE
	b_date >= '${b_date}' and mall_id = "864068930702966784"
	"""
}
