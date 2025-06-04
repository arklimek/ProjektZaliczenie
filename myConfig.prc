show-frame-rate-meter #f
sync-video #t
fullscreen #f
text-default-font Assets/Hud/SpaceMono.ttf
text-encoding utf8

#ifdef _WIN32
extern "C" {
  __declspec(dllexport) DWORD AmdPowerXpressRequestHighPerformance = 0x00000001;
  __declspec(dllexport) DWORD NvOptimusEnablement = 0x00000001;
}
#endif