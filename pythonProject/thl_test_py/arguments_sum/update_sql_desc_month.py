# -*- coding:utf-8 -*-

month_update = [
    {
        'delete_sql': """
DELETE FROM `dm_district_index_month`;
    """,
        'append_table': 'dm_district_index_month',
        'data_sql': """
SELECT
	t1.`month`
	,t1.source
	,'youth' as `type`
	,t1.index_sum as `index`
	,truncate((t1.index_sum - t2.index_sum)/t2.index_sum,18) as `index_ring_ratio`
	,t1.percent_sum as `percent`
	,truncate((t1.percent_sum - t2.percent_sum)/t2.percent_sum,18) as `percent_ring_ratio`
	
FROM
	(
	select
		s1.`month`,
		s1.source,
		s1.percent_sum,
		ROUND(s1.percent_sum * s2.`number`,0) as index_sum
	from
		(
		SELECT
			`month`
			,source
			,sum(`percent`) as percent_sum
		FROM
			dm_consumer_image_month
		WHERE
			image = 'age'
			and
			label IN ('18-24岁','25-34岁','35-44岁')
			and
			source <> ""
		GROUP BY
			`month`,source
		)s1
		INNER JOIN
		(
		SELECT
			`month`,
			source,
			`number`
		FROM
			dm_consumer_flow_arrive_month
		)s2 ON s1.`month` = s2.`month` AND s1.source = s2.source
	) t1 
	LEFT JOIN
	(
	select
		s1.`month`,
		s1.source,
		s1.percent_sum,
		ROUND(s1.percent_sum * s2.`number`,0) as index_sum
	from
		(
		SELECT
			`month`
			,source
			,sum(`percent`) as percent_sum
		FROM
			dm_consumer_image_month
		WHERE
			image = 'age'
			and
			label IN ('18-24岁','25-34岁','35-44岁')
			and
			source <> ""
		GROUP BY
			`month`,source
		)s1
		INNER JOIN
		(
		SELECT
			`month`,
			source,
			`number`
		FROM
			dm_consumer_flow_arrive_month
		)s2 ON s1.`month` = s2.`month` AND s1.source = s2.source
	) t2 ON str_to_date(CONCAT(t1.`month`,'01'),'%Y%m%d') = DATE_ADD(str_to_date(CONCAT(t2.`month`,'01'),'%Y%m%d'),INTERVAL 1 MONTH) AND t1.source = t2.source

UNION ALL

SELECT
	t1.`month`
	,t1.source
	,'female' as `type`
	,t1.index_sum as `index`
	,truncate((t1.index_sum - t2.index_sum)/t2.index_sum,18) as `ring_ratio`
	,t1.percent_sum as `percent`
	,truncate((t1.percent_sum - t2.percent_sum)/t2.percent_sum,18) as `percent_ring_ratio`
	
FROM
	(
	select
		s1.`month`,
		s1.source,
		s1.percent_sum,
		ROUND(s1.percent_sum * s2.`number`,0) as index_sum
	from
		(
		SELECT
			`month`
			,source
			,SUM(`percent`) as percent_sum
		FROM
			dm_consumer_image_month
		WHERE
			image = 'sex'
			and
			label = '女'
			and
			source <> ""
		GROUP BY
			`month`,source
		)s1
		INNER JOIN
		(
		SELECT
			`month`,
			source,
			`number`
		FROM
			dm_consumer_flow_arrive_month
		) s2 ON s1.`month` = s2.`month` AND s1.source = s2.source
	) t1 
	LEFT JOIN
	(
	select
		s1.`month`,
		s1.source,
		s1.percent_sum,
		ROUND(s1.percent_sum * s2.`number`,0) as index_sum
	from
		(
		SELECT
			`month`
			,source
			,SUM(`percent`) as percent_sum
		FROM
			dm_consumer_image_month
		WHERE
			image = 'sex'
			and
			label = '女'
			and
			source <> ""
		GROUP BY
			`month`,source
		)s1
		INNER JOIN
		(
		SELECT
			`month`,
			source,
			`number`
		FROM
			dm_consumer_flow_arrive_month
		) s2 ON s1.`month` = s2.`month` AND s1.source = s2.source
	) t2 ON str_to_date(CONCAT(t1.`month`,'01'),'%Y%m%d') = DATE_ADD(str_to_date(CONCAT(t2.`month`,'01'),'%Y%m%d'),INTERVAL 1 MONTH) AND t1.source = t2.source

UNION ALL

SELECT
	t1.month_6 as `month`
	,t1.source
	,'night' as `type`
	,t1.index_sum as `index`
	,truncate((t1.index_sum - t2.index_sum)/t2.index_sum,18) as `ring_ratio`
	,t1.percent_sum as `percent`
	,truncate((t1.percent_sum - t2.percent_sum)/t2.percent_sum,18) as `percent_ring_ratio`
	
FROM
	(
	SELECT
		s1.month_6
		,s1.source
		,s1.percent_sum
		,ROUND(s1.percent_sum * s2.`number`,0) as index_sum
	FROM
		(
		-- 整个商圈&游客&商综的占比
		SELECT
			date_format(date_sub(str_to_date(CONCAT(`date`,' ',`hour`),'%Y-%m-%d %H'),INTERVAL 6 HOUR),'%Y%m') as month_6
			,source
			,truncate(sum(IF((`hour`>=18 and `hour`<=23) or (`hour`>=0 and `hour`<=5),`number`,0))/sum(`number`),18) as percent_sum
		FROM
			dm_consumer_flow_arrive_hour
		WHERE
			source <> ""
		GROUP BY
			month_6,source
		)s1 
		inner join 
		(
		SELECT
			`month`,
			source,
			`number`
		FROM
			dm_consumer_flow_arrive_month
		) s2 ON s1.month_6 = s2.`month` AND s1.source = s2.source
	WHERE
		s1.month_6 <> date_format(curdate(),'%Y%m') and s1.month_6 <> '202012'
	) t1 
	LEFT JOIN
	(
	SELECT
		s1.month_6
		,s1.source
		,s1.percent_sum
		,ROUND(s1.percent_sum * s2.`number`,0) as index_sum
	FROM
		(
		-- 整个商圈&游客&商综的占比
		SELECT
			date_format(date_sub(str_to_date(CONCAT(`date`,' ',`hour`),'%Y-%m-%d %H'),INTERVAL 6 HOUR),'%Y%m') as month_6
			,source
			,truncate(sum(IF((`hour`>=18 and `hour`<=23) or (`hour`>=0 and `hour`<=5),`number`,0))/sum(`number`),18) as percent_sum
		FROM
			dm_consumer_flow_arrive_hour
		WHERE
			source <> ""
		GROUP BY
			month_6,source
		)s1 
		inner join 
		(
		SELECT
			`month`,
			source,
			`number`
		FROM
			dm_consumer_flow_arrive_month
		) s2 ON s1.month_6 = s2.`month` AND s1.source = s2.source
	WHERE
		s1.month_6 <> date_format(curdate(),'%Y%m') and s1.month_6 <> '202012'
	) t2 ON str_to_date(CONCAT(t1.`month_6`,'01'),'%Y%m%d') = DATE_ADD(str_to_date(CONCAT(t2.`month_6`,'01'),'%Y%m%d'),INTERVAL 1 MONTH) AND t1.source = t2.source
    """
    },
    {
        'delete_sql': """
DELETE FROM `dm_visits_times_month_business`;
    """,
        'append_table': 'dm_visits_times_month_business',
        'data_sql': """
SELECT
	s1.`month`,
	TRUNCATE(s1.sum_once/s2.`number`,15) as once,
	TRUNCATE(s1.sum_twice/s2.`number`,15) as twice,
	TRUNCATE(s1.sum_thrice/s2.`number`,15) as thrice,
	TRUNCATE(s1.sum_over_thrice/s2.`number`,15) as over_thrice,
	0 as avg_times
FROM
	(
	-- 算得每个商综停留X天的人数
	SELECT
		t2.`month`,
		sum(t1.number*t2.once) as sum_once,
		sum(t1.number*t2.twice) as sum_twice,
		sum(t1.number*t2.thrice) as sum_thrice,
		sum(t1.number*t2.over_thrice) as sum_over_thrice
	FROM
		dm_source_percent_num_month t1
		INNER JOIN dm_visits_times_month t2 
		ON (t1.`month_2` = t2.`month` and t1.source = t2.source)
	GROUP BY
		t2.`month`
	) s1
	INNER JOIN 
	(
	SELECT
		month_2 as `month`,
		sum(`number`) as `number`
	FROM
		dm_source_percent_num_month
	WHERE
		source <> "all"
	GROUP BY
		month_2
	) s2
	ON s1.`month` = s2.`month`
    """
    },
    {
        'delete_sql': """
DELETE FROM `dm_origin_index_percent_month`;
    """,
        'append_table': 'dm_origin_index_percent_month',
        'data_sql': """
with t as (
SELECT
	date_format(str_to_date(t1.`month`,'%Y%m'),'%Y-%m') as `month`,
	t1.source,
	t1.`type`,
	ROUND(t1.`percent`*t2.`number`,0) as `index`,
	TRUNCATE(t1.`percent`,18) as `percent`,
	t2.`number` as `month_number`
FROM
	(
	SELECT
		`month`,
		source,
		'guangzhou_inside' as `type`,
		SUM(`percent`) as `percent`
	FROM
		dm_district_image_geo_month
	WHERE
		`image` = "residentCity" and label = "residentCity" and `value` = '广州市'
		and
		source <> ""
	GROUP BY
		`month`,source
		
	UNION ALL
	
	-- 此处的广东省内，去除了广州
	SELECT
		s1.`month`,
		s1.source,
		'guangdong_inside' as `type`,
		(s1.`percent`-s2.`percent`) as `percent`
	FROM
		(
		SELECT
			`month`,
			source,
			SUM(`percent`) as `percent`
		FROM
			dm_district_image_geo_month
		WHERE
			`image` = "residentProvince" and label = "residentProvince" and `value` = '广东省'
			and
			source <> ""
		GROUP BY
			`month`,source
		) s1
		INNER JOIN
		(
		SELECT
			`month`,
			source,
			SUM(`percent`) as `percent`
		FROM
			dm_district_image_geo_month
		WHERE
			`image` = "residentCity" and label = "residentCity" and `value` = '广州市'
			and
			source <> ""
		GROUP BY
			`month`,source
		) s2 ON s1.`month` = s2.`month` and s1.source = s2.source
		
	UNION ALL
	
	-- 此处1-广东省作为省外
	SELECT
		`month`,
		source,
		'guangdong_outside' as `type`,
		1-SUM(`percent`) as `percent`
	FROM
		dm_district_image_geo_month
	WHERE
		`image` = "residentProvince" and label = "residentProvince" and `value` = '广东省'
		and
		source <> ""
	GROUP BY
		`month`,source
	) t1 INNER JOIN
	(
	SELECT
		`month`,
		source,
		`number`
	FROM
		dm_consumer_flow_arrive_month
	)t2 ON t1.`month` = t2.`month` and t1.source = t2.source
)
SELECT
	t1.`month`,
	t1.source,
	t1.`type`,
	t1.`index`,
	t1.`percent`,
	t2.`index` as last_index,
	t2.`percent` as last_percent,
	t3.`index` as last_year_index,
	t3.`percent` as last_year_percent,
	truncate((t1.`index`-t2.`index`)/t2.`index`,18) as index_ring_ratio,
	truncate((t1.`index`-t3.`index`)/t3.`index`,18) as index_year_ratio,
	t1.`month_number`
FROM
	t t1 
	LEFT JOIN 
	t t2 ON str_to_date(CONCAT(t1.`month`,'-01'),'%Y-%m-%d') = DATE_ADD(str_to_date(CONCAT(t2.`month`,'-01'),'%Y-%m-%d'),INTERVAL 1 MONTH) and t1.source = t2.source and t1.`type` = t2.`type`
	LEFT JOIN 
	t t3 ON str_to_date(CONCAT(t1.`month`,'-01'),'%Y-%m-%d') = DATE_ADD(str_to_date(CONCAT(t3.`month`,'-01'),'%Y-%m-%d'),INTERVAL 12 MONTH) and t1.source = t3.source and t1.`type` = t3.`type`
    """
    },
    {
        'delete_sql': """
DELETE FROM `dm_origin_index_city_month`;
    """,
        'append_table': 'dm_origin_index_city_month',
        'data_sql': """
SELECT
	s1.`month`,
	s1.source,
	(CASE
	WHEN s3.city_name IS NOT NULL THEN "省内"
	WHEN s3.city_name IS NULL THEN "省外"
	END) as city_type,
	s1.city,
	ROUND(s2.`number`*s1.`percent`,0) as `city_number`,
	truncate(s1.`percent`,18) as `city_percent`,
	s2.`number` as `month_number`
FROM
	(
	SELECT
		`month`,
		`source`,
		`value` as city,
		`percent`
	FROM
		dm_district_image_geo_month
	WHERE
		`image` = "residentCity" and label = "residentCity"
		and 
		`value` <> ""
	) s1
	INNER JOIN
	(
	SELECT
		`month`,
		source,
		`number`
	FROM
		dm_consumer_flow_arrive_month
	)s2 ON s1.`month` = s2.`month` and s1.`source` = s2.`source`
	LEFT JOIN 
	dim_guangdong_city_name s3 on s1.city = s3.city_name 
    """
    },
    {
        'delete_sql': """
DELETE FROM `dm_province_index_month`;
    """,
        'append_table': 'dm_province_index_month',
        'data_sql': """
SELECT
	date_format(str_to_date(s1.`month`,'%Y%m'),'%Y-%m') as `month`,
	s1.source,
	s1.province,
	ROUND(s2.`number`*s1.`percent`,0) as `number`

FROM
	(
	select 
		`month`,
		source,
		`value` as province,
		`percent`
	from 
		dm_district_image_geo_month
	WHERE
		`image` = "residentProvince" and label = "residentProvince"
		and
		`value` <> ""
		and
		source <> ""
	) s1
	INNER JOIN
	(
	SELECT
		`month`,
		source,
		`number`
	FROM
		dm_consumer_flow_arrive_month
	)s2 ON s1.`month` = s2.`month` and s1.source = s2.source
    """
    },
    {
        'delete_sql': """
DELETE FROM	`dm_mobile_terminal_app_top10`;
    """,
        'append_table': 'dm_mobile_terminal_app_top10',
        'data_sql': """
select
    '678' as `id`,
    case
        when `t1`.`rank` = 1 then 'YDDSYPH_TOP1'
        when `t1`.`rank` = 2 then 'YDDSYPH_TOP2'
        when `t1`.`rank` = 3 then 'YDDSYPH_TOP3'
        when `t1`.`rank` = 4 then 'YDDSYPH_TOP4'
        when `t1`.`rank` = 5 then 'YDDSYPH_TOP5'
        when `t1`.`rank` = 6 then 'YDDSYPH_TOP6'
        when `t1`.`rank` = 7 then 'YDDSYPH_TOP7'
        when `t1`.`rank` = 8 then 'YDDSYPH_TOP8'
        when `t1`.`rank` = 9 then 'YDDSYPH_TOP9'
        when `t1`.`rank` = 10 then 'YDDSYPH_TOP10'
    end as `statistics_type`,
    '移动端使用偏好-TOP10APP' as `data_name`,
    replace(t1.`label`, 'APP安装', '') as `item_name`,
    t1.`index` as `value`,
    current_timestamp() as `created_time`,
    t1.`month` as `b_date`
from
    (
    select
        `month`,
        `label`,
        `index`,
        row_number() over ( partition by `month` order by `index` desc) as `rank`
    from
        dm_consumer_network_image_month
    where
        `image` = 'installApp'
        and 
		`source` = 'all'
	) t1
where
    t1.`rank` <= 10
    """
    },
    {
        'delete_sql': """
DELETE FROM	`dm_business_increase_month`;
    """,
        'append_table': 'dm_business_increase_month',
        'data_sql': """
with t as (
SELECT
	cast(t1.`month` as char) as `month`,
	truncate((ifnull(t1.number_index,0) + ifnull(t2.sum_index,0))*0.4 + ifnull(t3.gmv_index,0)*0.3 + ifnull(t4.sum_index,0)*0.3,18) as `index`
FROM
	(
	SELECT
		`month`,
		number_ring_ratio as number_index
	FROM
		dm_consumer_flow_arrive_month
	WHERE
		source = "all"
		and 
		-- 去除本月数据
		`month` <> date_format(now(),"%Y%m") 
	) t1
	LEFT JOIN
	(
	SELECT
		`month`,
		sum(index_ring_ratio) as sum_index
	FROM
		dm_district_index_month
	WHERE
		source = "all"
		and
		`type` IN ("female","night","youth")
	GROUP BY
		`month`
	) t2 ON CAST(t1.`month` as char) = t2.`month`
	LEFT JOIN
	(
	SELECT
		s1.`month`,
		truncate((s1.gmv-s2.gmv)/s2.gmv,18) as gmv_index
	FROM
		dm_ta_order_target_month s1
		LEFT JOIN
		dm_ta_order_target_month s2 ON str_to_date(CONCAT(s1.`month`,'01'),'%Y%m%d') = DATE_ADD(str_to_date(CONCAT(s2.`month`,'01'),'%Y%m%d'),INTERVAL 1 MONTH)
	) t3 ON CAST(t1.`month` as char) = t3.`month`
	LEFT JOIN
	(
	SELECT
		date_format(str_to_date(CONCAT(`month`,'-01'),'%Y-%m-%d'),'%Y%m') as month_2,
		sum(index_ring_ratio) as sum_index
	FROM
		dm_origin_index_percent_month
	WHERE
		source = "all"
		and
		`type` IN ("guangdong_inside","guangdong_outside","guangzhou_inside")
		and
		index_ring_ratio IS NOT NULL
	GROUP BY
		month_2
	)t4 ON CAST(t1.`month` as char) = t4.month_2
)

SELECT
	t1.`month`,
	t1.`index`,
	-- 若除数等于0或者为空，则置0；若除数小于0，则取其绝对值；
	(CASE
	when (t2.`index`=0 or t2.`index` is null) then 0
	when t2.`index`<0 then truncate((t1.`index`-t2.`index`)/(-t2.`index`),18)
	else truncate((t1.`index`-t2.`index`)/t2.`index`,18)
	END) as index_ring_ratio
FROM
	t t1
	LEFT JOIN t t2 ON str_to_date(CONCAT(t1.`month`,'01'),'%Y%m%d') = DATE_ADD(str_to_date(CONCAT(t2.`month`,'01'),'%Y%m%d'),INTERVAL 1 MONTH)
    """
    },
    {
        'delete_sql': """
DELETE FROM `dm_consumer_image_month_ratio`;
    """,
        'append_table': 'dm_consumer_image_month_ratio',
        'data_sql': """
with t as (
select 
	`month`,
	`image`,
	`label`,
	`percent`,
	`index`,
	`source`
FROM
	dm_consumer_image_month
)

SELECT
	t1.`month`,
	t1.`image`,
	t1.`label`,
	t1.`percent`,
	if((t2.`percent`=0 or t2.`percent` is null),0,truncate((t1.`percent`-t2.`percent`)/t2.`percent`,18)) as percent_ring_ratio,
	t1.`index`,
	if((t2.`index`=0 or t2.`index` is null),0,truncate((t1.`index`-t2.`index`)/t2.`index`,18)) as index_ring_ratio,
	t1.`source`
FROM
	t t1
	LEFT JOIN t t2 
	ON (t1.`month` = date_format(date_add(str_to_date(CONCAT(t2.`month`,"01"),"%Y%m%d"),INTERVAL 1 MONTH),"%Y%m") and t1.`image` = t2.`image` and t1.`label` = t2.`label` and t1.`source` = t2.`source`)
    """
    },
    {
        'delete_sql': """
DELETE FROM `unionpay_statistics_day_formats`;
    """,
        'append_table': 'unionpay_statistics_day_formats',
        'data_sql': """
SELECT
	"678" as `id`,
	"id_guangzhou_tianhelu" as circle_id,
	CONCAT("no00",t1.week_num) as week_number,
	IF(t1.week_day = "0","7",t1.week_day) as week_day,
	(CASE 
	WHEN t2.b_type IN ("彩妆护肤","次主力店","家具家电","品牌服饰","珠宝首饰","综合零售") THEN "1"
	WHEN t2.b_type = "美食餐饮" THEN "2"
	WHEN t2.b_type = "休闲运动" THEN "4"
	WHEN t2.b_type = "娱乐体验" THEN "5"
	ELSE "6"
	END) as service_type,
	t1.gmv as tr_amt,
	SUM(t1.order_count) as tr_num,
	0 as tr_card,
	now() as created_time,
	date_format(t1.`day`,"%Y%m%d") as b_date
FROM
	(
	select
		date_format(`create_at`,'%v') as `week_num`,
		date_format(`create_at`,'%w') as `week_day`,
		date(`create_at`) as `day`,
		store_num,
		store_name,
		count(order_num) as order_count,
		sum(amount) as gmv
	FROM
		zhengjia_sale_data
	WHERE
		pay_status = "交易成功"
	GROUP BY
		`day`,store_num,store_name
	)t1
	INNER JOIN dm_store_b_type_info t2 
	ON t1.store_num = t2.store_num and t1.store_name = t2.store_name
GROUP BY
	b_date,service_type
	
UNION ALL

SELECT
	"678" as `id`,
	"id_guangzhou_tianhelu" as circle_id,
	CONCAT("no00",t1.week_num) as week_number,
	IF(t1.week_day = "0","7",t1.week_day) as week_day,
	"0" as service_type,
	t1.gmv as tr_amt,
	SUM(t1.order_count) as tr_num,
	0 as tr_card,
	now() as created_time,
	date_format(t1.`day`,"%Y%m%d") as b_date
FROM
	(	
	select
		date_format(`day`,'%v') as `week_num`,
		date_format(`day`,'%w') as `week_day`,
		`day`,
		order_count,
		gmv
	FROM
		dm_order_target_day
	)t1
GROUP BY
	b_date
    """
    }
]
