{
   "variables": {
    'openssl_fips': ''
  },
  'targets': [
    {
      'target_name': 'keytar',
      'dependencies': [
        "<!(node -p \"require('node-addon-api').targets\"):node_addon_api",
      ],
      'defines': [
        "NAPI_VERSION=<(napi_build_version)",
      ],
      'cflags!': [ '-fno-exceptions' ],
      'cflags_cc!': [ '-fno-exceptions' ],
      'xcode_settings': {
        'GCC_ENABLE_CPP_EXCEPTIONS': 'YES',
        'CLANG_CXX_LIBRARY': 'libc++',
        'MACOSX_DEPLOYMENT_TARGET': '10.7',
        'OTHER_CFLAGS': [
          "-std=c++17",
          "-stdlib=libc++"
        ],
      },
      'msvs_settings': {
        'VCCLCompilerTool': {
          'ExceptionHandling': 1,
          'AdditionalOptions': [
            '/Qspectre',
            '/guard:cf'
          ]
        },
        'VCLinkerTool': {
          'AdditionalOptions': [
            '/guard:cf'
          ]
        }
      },
      'include_dirs': ["<!(node -p \"require('node-addon-api').include_dir\")"],
      'sources': [
        'src/native/async.cc',
        'src/native/main.cc',
        'src/native/keytar.h',
        'src/native/credentials.h',
      ],
      'conditions': [
        ['OS=="mac"', {
          'sources': [
            'src/native/keytar_mac.cc',
          ],
          'link_settings': {
            'libraries': [
              '$(SDKROOT)/System/Library/Frameworks/AppKit.framework',
            ],
          },
        }],
        ['OS=="win"', {
          'sources': [
            'src/native/keytar_win.cc',
          ],
          'msvs_disabled_warnings': [
            4267,  # conversion from 'size_t' to 'int', possible loss of data
            4530,  # C++ exception handler used, but unwind semantics are not enabled
            4506,  # no definition for inline function
          ],
        }],
        ['OS not in ["mac", "win"]', {
          'sources': [
            'src/native/keytar_posix.cc',
          ],
          'cflags': [
            '<!(pkg-config --cflags libsecret-1)',
            '-Wno-missing-field-initializers',
            '-Wno-deprecated-declarations',
          ],
          'link_settings': {
            'ldflags': [
              '<!(pkg-config --libs-only-L --libs-only-other libsecret-1)',
            ],
            'libraries': [
              '<!(pkg-config --libs-only-l libsecret-1)',
            ],
          },
        }]
      ],
    }
  ]
}
