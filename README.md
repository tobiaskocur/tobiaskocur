<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:0d1117,100:1F2228&height=150&section=header&text=&fontSize=40&animation=fadeIn" width="100%"/>
</div>

<div align="center">
  <h1 style="border-bottom: none;">Tobias | Systems & Security Engineer</h1>
  <p>🇸🇰 Slovakia &nbsp;•&nbsp; System Security &nbsp;•&nbsp; Kernel Development &nbsp;•&nbsp; Reverse Engineering</p>
  <p><i>"Security through opacity is not security. I break systems to build them stronger."</i></p>
</div>

<br/>

<div align="center">
  <a href="https://www.linkedin.com/in/tobias-kocúr-3b18b63b5">
    <img src="https://img.shields.io/badge/Focus-Low--Level_Systems_%26_Security-1F2228?style=for-the-badge&logo=linux&logoColor=white"/>
  </a>
  <a href="mailto:crybybusiness@gmail.com">
    <img src="https://img.shields.io/badge/Open_To-Internships_%26_Research_Collabs-success?style=for-the-badge&logo=protonmail&logoColor=white"/>
  </a>
</div>

<br/>

<div align="center">
  <img src="https://img.shields.io/badge/Goal-University_Applications_(2026)-b45309?style=for-the-badge&logo=academia&logoColor=white"/>
</div>

<br/>

<div align="center">
  <img src="https://readme-typing-svg.demolab.com/?font=JetBrains+Mono&size=18&duration=2500&pause=1000&color=569CD6&center=true&vCenter=true&width=760&lines=Analyzing+Windows+Kernel+Internals;Reverse+Engineering+iOS+Device+Protocols;Building+Integrity+%26+Anti-Tamper+Tooling;Learning+by+debugging+real+systems" />
</div>

<br/>

<h2 align="center">Technical Arsenal</h2>

<div align="center">
  <table>
    <tr align="center">
      <td width="33%"><b>Core Engineering</b></td>
      <td width="33%"><b>System Internals</b></td>
      <td width="33%"><b>Analysis & Debugging</b></td>
    </tr>
    <tr align="center">
      <td>
        <img src="https://img.shields.io/badge/C++17%2F20-00599C?style=flat-square&logo=cplusplus&logoColor=white" /><br/><br/>
        <img src="https://img.shields.io/badge/C_(Systems)-A8B9CC?style=flat-square&logo=c&logoColor=black" /><br/><br/>
        <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" />
      </td>
      <td>
        <img src="https://img.shields.io/badge/Windows_Kernel-0078D6?style=flat-square&logo=windows&logoColor=white" /><br/><br/>
        <img src="https://img.shields.io/badge/x64_Assembly-0071C5?style=flat-square&logo=intel&logoColor=white" /><br/><br/>
        <img src="https://img.shields.io/badge/WDK_%2F_Drivers-FFA500?style=flat-square&logo=windowsterminal&logoColor=white" />
      </td>
      <td>
        <img src="https://img.shields.io/badge/IDA_Pro-1F2228?style=flat-square&logo=hackthebox&logoColor=white" /><br/><br/>
        <img src="https://img.shields.io/badge/x64dbg-1aa1fd?style=flat-square&logo=windowsterminal&logoColor=white" /><br/><br/>
        <img src="https://img.shields.io/badge/WinDbg-4D4D4D?style=flat-square&logo=windows&logoColor=white" />
      </td>
    </tr>
  </table>
</div>

<br/>

<div align="center">
  <img src="https://i.imgur.com/JYXkEF2.png" alt="BSOD" width="90%" style="border-radius: 6px; border: 1px solid #30363d;" />
  <br/>
  <i>POV: You acquired the spinlock at <code>DISPATCH_LEVEL</code> but touched paged memory...</i>
</div>

<br/>

## Deep-Dive Projects

### <img src="https://img.shields.io/badge/-Aegis-0078D6?style=flat-square&logo=windows&logoColor=white"/> &nbsp;[Aegis](https://github.com/tobiaskocur/aegis) &nbsp;|&nbsp; Kernel Protection Driver (PoC)
A kernel-mode driver focused on reducing user-mode tampering against protected processes.
- **Access Control:** Uses `ObRegisterCallbacks` to filter/strip handle permissions.
- **Hardening (WIP):** Researching safe kernel telemetry + anti-tamper patterns (no "magic stealth claims").
- **Stack:** `C` &nbsp;`WDK` &nbsp;`Kernel synchronization` &nbsp;`IRQL-aware code`

---

### <img src="https://img.shields.io/badge/-Mindly-000000?style=flat-square&logo=apple&logoColor=white"/> &nbsp;[Mindly](https://github.com/tobiaskocur/mindly_dock) &nbsp;|&nbsp; iOS Protocol Tooling
A digital detox tool that interfaces with iOS devices over USB to enforce restriction profiles.
- **Protocol work:** Exploring iOS configuration / MDM-related workflows via `libimobiledevice`.
- **Implementation:** Desktop UX using `ImGui`, device control via USB stack.
- **Stack:** `C++` &nbsp;`USB protocols` &nbsp;`Reverse engineering mindset`

---

### <img src="https://img.shields.io/badge/-Sajko.sk-000000?style=flat-square&logo=nextdotjs&logoColor=white"/> &nbsp;[Sajko.sk](https://sajko.sk) &nbsp;|&nbsp; Session Replay Platform
Enterprise-grade session replay & analytics platform with a real-time event pipeline.
- **Pipeline:** Ingest → process → store → replay user sessions.
- **Stack:** `TypeScript` &nbsp;`Next.js` &nbsp;`PostgreSQL` &nbsp;`WASM`

---

## Current Research & Deep Dives
I learn systems security by debugging real artifacts and writing tooling around them:
- **Windows Internals:** scheduler, `EPROCESS/KTHREAD`, handle tables, callbacks
- **Kernel dev:** WDK, IRQL rules, sync primitives, IOCTL design
- **RE practice:** static + dynamic analysis, patching, small PoCs
- **Writing:** turning findings into writeups (planned: blog repo)

<br/>

### Code Glimpse
```c
#include <ntddk.h>

NTSTATUS DriverEntry(_In_ PDRIVER_OBJECT DriverObject, _In_ PUNICODE_STRING RegistryPath) {
    UNREFERENCED_PARAMETER(RegistryPath);

    DriverObject->DriverUnload = NULL;
    DbgPrintEx(DPFLTR_IHVDRIVER_ID, DPFLTR_INFO_LEVEL, "Aegis: Driver loaded.\n");

    return STATUS_SUCCESS;
}
```

<br/>

<h2 align="center">Uplink</h2>

<div align="center">
  <a href="mailto:crybybusiness@gmail.com">
    <img src="https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white" />
  </a>
  &nbsp;
  <a href="https://www.linkedin.com/in/tobias-kocúr-3b18b63b5">
    <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" />
  </a>
  &nbsp;
  <a href="https://github.com/tobiaskocur">
    <img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" />
  </a>
</div>

<br/>
