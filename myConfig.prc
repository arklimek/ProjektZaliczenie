show-frame-rate-meter #t
sync-video #f
text-default-font Assets/Hud/SpaceMono.ttf
text-encoding utf8
threading-model Cull/Draw
hardware-animated-vertices true
basic-shaders-only true
gl-immutable-texture-storage true
preload-simple-textures 1
text-anisotropic-degree 2

#ifdef _WIN32
extern "C" {
  __declspec(dllexport) DWORD AmdPowerXpressRequestHighPerformance = 0x00000001;
  __declspec(dllexport) DWORD NvOptimusEnablement = 0x00000001;
}
#endif