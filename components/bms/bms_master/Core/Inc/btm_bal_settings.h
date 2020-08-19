/**
 * @file Balancing_Skeleton.h
 *
 * @date Jun. 9, 2020
 *
 */

#ifndef INC_BTM_BAL_SETTINGS_H_
#define INC_BTM_BAL_SETTINGS_H_

#include "ltc6813_btm.h"
#include "ltc6813_btm_bal.h"

void BTM_BAL_settings(
    BTM_PackData_t* pack,
    BTM_BAL_dch_setting_pack_t* dch_setting_pack);

#endif /* INC_BTM_BAL_SETTINGS_H_ */
