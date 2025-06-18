"use client";

import { FC } from "react";
import { observer } from "mobx-react";
import { Inbox } from "lucide-react";
import { useTranslation } from "@plane/i18n";
import { Breadcrumbs, Header } from "@plane/ui";
// components
import { BreadcrumbLink } from "@/components/common";
import { SidebarHamburgerToggle } from "@/components/core";
import { NotificationSidebarHeaderOptions } from "@/components/workspace-notifications";
// hooks
import { useAppTheme } from "@/hooks/store";
// plane web components
import { isSidebarToggleVisible } from "@/plane-web/components/desktop";

type TNotificationSidebarHeader = {
  workspaceSlug: string;
};

export const NotificationSidebarHeader: FC<TNotificationSidebarHeader> = observer((props) => {
  const { workspaceSlug } = props;
  const { t } = useTranslation();
  const { sidebarCollapsed } = useAppTheme();

  if (!workspaceSlug) return <></>;
  return (
    <Header className="my-auto bg-custom-background-100">
      <Header.LeftItem>
        {sidebarCollapsed && <SidebarHamburgerToggle />}

        {isSidebarToggleVisible() && (
          <div className="block bg-custom-sidebar-background-100 md:hidden">
            <SidebarHamburgerToggle />
          </div>
        )}
        <Breadcrumbs>
          <Breadcrumbs.BreadcrumbItem
            type="text"
            link={
              <BreadcrumbLink
                label={t("notification.label")}
                icon={<Inbox className="h-4 w-4 text-custom-text-300" />}
                disableTooltip
              />
            }
          />
        </Breadcrumbs>
      </Header.LeftItem>
      <Header.RightItem>
        <NotificationSidebarHeaderOptions workspaceSlug={workspaceSlug} />
      </Header.RightItem>
    </Header>
  );
});
