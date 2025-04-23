show-frame-rate-meter #t
sync-video #f

#ifdef _WIN32
extern "C" {
  __declspec(dllexport) DWORD AmdPowerXpressRequestHighPerformance = 0x00000001;
  __declspec(dllexport) DWORD NvOptimusEnablement = 0x00000001;
}
#endif