areg n_female_minister literacy_suffrage_restriction democracy gender_suffrage_restriction opposition, absorb(country_isocode) cluster(country_isocode )

areg n_female_total literacy_suffrage_restriction democracy gender_suffrage_restriction opposition, absorb(country_isocode) cluster(country_isocode )

gen adj_n_female_total = n_female_total + 0.01

gen ln_female_total = log(adj_n_female_total  )

areg ln_female_total literacy_suffrage_restriction democracy gender_suffrage_restriction opposition, absorb(country_isocode) cluster(country_isocode )

areg retention_rate_total n_female_total leaderexperience_total democracy age_total female_leader, absorb(country_isocode ) cluster(country_isocode )


* 25 April
*=============

* 1. Simple Model: Effect on number of females in politics (total, minister and core) due to effects of democracy, suffrage, female head and an opposition

reg n_female_total democracy fullsuffrage female opposition
areg n_female_total democracy fullsuffrage female opposition, absorb(country_isocode) cluster(country_isocode) // High R^2
 
reg n_female_minister democracy fullsuffrage female opposition
areg n_female_minister democracy fullsuffrage female opposition, absorb(country_isocode) cluster(country_isocode) // High R^2

reg n_female_core democracy fullsuffrage female opposition
areg n_female_core democracy fullsuffrage female opposition, absorb(country_isocode) cluster(country_isocode) // High R^2


* 2. Adding Variables:  number of parties, suffrage restrictions, winning party share, average age of cabinet, leaderexperience_total
* Removing Variables: Opposition, suffrage

reg n_female_total democracy female n_party gender_suffrage_restriction ethnic_racial_suffrage_restricti literacy_suffrage_restriction wealth_suffrage_restriction other_suffrage_restriction party_share age_total leaderexperience_total

areg n_female_total democracy female n_party gender_suffrage_restriction ethnic_racial_suffrage_restricti literacy_suffrage_restriction wealth_suffrage_restriction other_suffrage_restriction party_share age_total leaderexperience_total, absorb(country_isocode) cluster(country_isocode) // High R^2

areg n_female_minister democracy female n_party gender_suffrage_restriction ethnic_racial_suffrage_restricti literacy_suffrage_restriction wealth_suffrage_restriction other_suffrage_restriction party_share age_total leaderexperience_total, absorb(country_isocode) cluster(country_isocode) // Democracy starts to have a lesser +ve impact

areg n_female_core democracy female n_party gender_suffrage_restriction ethnic_racial_suffrage_restricti literacy_suffrage_restriction wealth_suffrage_restriction other_suffrage_restriction party_share age_total leaderexperience_total, absorb(country_isocode) cluster(country_isocode) // Democracy starts to have a lesser +ve impact


* 3. Interaction Terms

foreach var of varlist female opposition leaderexperience_total{
	gen inter_dem_`var' = `var' * democracy
}

areg n_female_core democracy female inter_dem_female, absorb(country_isocode ) cluster(country_isocode ) // High R^2 but interaction :x
reg n_female_total democracy female leaderexperience_total inter_dem_female inter_dem_leaderExp_female inter_female_leaderExp inter_dem_leaderexperience_total 

areg n_female_minister democracy female leaderexperience_total inter_dem_female inter_dem_leaderExp_female inter_female_leaderExp inter_dem_leaderexperience_total , absorb(country_isocode ) cluster (country_isocode )

areg n_female_total leaderexperience_total female inter_female_leaderExp, cluster(country_isocode ) absorb(country_isocode )

gen inter_fem_total = female * n_female_total
areg average_total n_female_total female inter_fem_total, absorb(country_name) cluster(country_name)

areg leaderexperience_continuous n_female_total female inter_fem_total, absorb(country_name) cluster(country_name)

gen pre2000 = 0
replace pre2000 = 1 if year < 2000
gen inter_dem_time = democracy * pre2000 
reg n_female_total democracy pre2000 inter_dem_time 
areg n_female_share  democracy pre2000 inter_dem_time, absorb(country_isocode ) cluster(country_isocode )

* 4. Retension Rates

* If females are increasing with retension rates going down, it means old policy makers are being replaced with a less mysoginistic crowd
areg n_female_total democracy retention_rateadj_total female n_party gender_suffrage_restriction ethnic_racial_suffrage_restricti literacy_suffrage_restriction wealth_suffrage_restriction other_suffrage_restriction party_share age_total leaderexperience_total, absorb(country_isocode) cluster(country_isocode) // High R^2 and +ve Relation

* Trend needs to be captured of increased retension rate


* 1 May
*=============

areg n_female_total_adjusted democracy female opposition v2paminor v2xpa_illiberal v2palgbt v2parelig v2pawomlab v2paculsup v2paopresp v2paviol, absorb(country_isocode )
* minority is negative: intersectionality and motivation argument




