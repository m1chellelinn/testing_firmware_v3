/**
 *  @file pack.h
 *  @brief Header file for driver for LTC6813-1 pack data monitoring
 *
 *  @date 2023/03/18
 *  @author Tigran Hakobyan (Tik-Hakobyan)
 */

#ifndef INC_PACK_H_
#define INC_PACK_H_

#include <stdint.h>

/*============================================================================*/
/* PUBLIC CONSTANTS */
// Do not change

#define PACK_NUM_BATTERY_MODULES 32

/*============================================================================*/
/* STRUCTURES FOR GATHERED DATA */

/*
 * NOTE: the Pack_module entity would be considered a "cell" by the LTC6813
 * datasheet's naming conventions. Here it's called a module due to the fact
 * that we arrange physical battery cells in parallel to create modules.
 * (the cells in a module are in parallel - they're all at the same voltage
 * and their voltage is measured at the module, not cell level).
 */
typedef struct{

    uint16_t voltage; // stored in the same format it is received from the LTC6813 in
    float temperature;
    int status;

}  Pack_module;

typedef struct {
    
    Pack_module module [PACK_NUM_BATTERY_MODULES];
    int status; //intended to be the summary of fault/warning/trip flags
    
} PackData_t;

typedef struct{

    uint32_t stackNum;
    uint32_t cellNum;

} ModuleIndex_t;

extern const ModuleIndex_t module_mapping[];

#endif // INC_PACK_H_