import React from "react";

export default function MainContent() {
  return (
    <div className="px-40 flex flex-1 justify-center py-5">
      <div className="layout-content-container flex flex-col max-w-[960px] flex-1">
        <div className="@container">
          <div className="@[480px]:p-4">
            <div
              className="flex min-h-[480px] flex-col gap-6 bg-cover bg-center bg-no-repeat @[480px]:gap-8 @[480px]:rounded-xl items-center justify-center p-4"
              style={{
                backgroundImage:
                  'linear-gradient(rgba(0, 0, 0, 0.1) 0%, rgba(0, 0, 0, 0.4) 100%), url("https://lh3.googleusercontent.com/aida-public/AB6AXuD-pUQuRj9kquC8iiO_GC9sKDKUBGRiBCJRLyvAK_wiWmRTb7Ix6pjJ-qjR2DMt0P8aF5uzu8eGY0I_CPqo7bG9PMWs5IT8sZjQHSpA3u6SndAFPL5MLY3S3wWsQHKf8aFg4eipX6p0PQOHOt7iPFKz-OG5FXUSpqJDrlPw4CS_KLT05zQdzFs1sFvoPRKScWwZeI2uTWqN5XH_-hsUqvNaMNa_BIvOL4clxgqlVyg3180z9V0heB0YicXAWhN3ag_BALl_RP6W6AI")',
              }}
            >
              <div className="flex flex-col gap-2 text-center">
                <h1 className="text-white text-4xl font-black leading-tight tracking-[-0.033em] @[480px]:text-5xl @[480px]:font-black @[480px]:leading-tight @[480px]:tracking-[-0.033em]">
                  Connect with your community
                </h1>
                <h2 className="text-white text-sm font-normal leading-normal @[480px]:text-base @[480px]:font-normal @[480px]:leading-normal">
                  Connect is where you can make a home for your communities and friends. Where you can stay close and have fun over text, voice, and video.
                </h2>
              </div>
              <button
                className="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-full h-10 px-4 @[480px]:h-12 @[480px]:px-5 bg-[#d7e6f3] text-[#101519] text-sm font-bold leading-normal tracking-[0.015em] @[480px]:text-base @[480px]:font-bold @[480px]:leading-normal @[480px]:tracking-[0.015em]"
              >
                <span className="truncate">Try the App</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}