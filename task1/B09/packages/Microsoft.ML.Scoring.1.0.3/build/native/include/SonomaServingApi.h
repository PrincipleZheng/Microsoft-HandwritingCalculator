#pragma once

#ifdef SONOMASERVING_DLL
    #ifdef SONOMASERVING_DLL_EXPORT
        #define SONOMASERVING_API __declspec(dllexport)
    #else
        #define SONOMASERVING_API __declspec(dllimport)
    #endif
#else
    #define SONOMASERVING_API
#endif