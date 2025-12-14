# Luciver Status Sheet

Luciver is the Discord concierge for the Lumina dev server. It reacts to natural language cues that include its name, moves messages between channels, keeps running task and reminder lists, and reports weekly summaries for moderators.

## Live Commands & Triggers

| Trigger | Example | Result |
| --- | --- | --- |
| `luciver help` | Luciver help | Posts the help embed with every available shortcut. |
| `luciver ping #channel [note]` | Luciver ping #design and #frontend the above image with the note rough flow ready. | Forwards the message you replied to (or the last non-bot message when you say “above message”) into every tagged channel; attaches the author’s note if provided. |
| `luciver assign @user <task>` | Luciver assign @Nova finish responsive tweaks | (Moderators only) logs the task, posts the record in #luciver-log, and queues it for the Sunday digest. |
| `luciver delete/remove the above <n> messages` | Luciver delete the above 3 messages | (Moderators only) removes up to 20 recent, unpinned messages in the channel so sensitive chatter can be cleared quickly (skips anything older than 14 days). |
| `luciver remind me/<@user>/<@&role>/@everyone <note + time>` | Luciver remind @everyone prep release notes at 17:00 | Handles phrases like `in 20m`, `tomorrow 5pm`, `at 4:40am`, or `17 Dec 09:00`, schedules the reminder, confirms the ETA, and logs the entry for audit (defaults to 09:00 if you omit a time). Group targets fan out to direct messages for every member. |
| `luciver stats` (also `status`, `pulse`) | Luciver stats | Summarises total traffic, top channels, top contributors, quiet channels, operations snapshot (tasks + reminders), and the Moderator / Others headcount. |
| `@Luciver` inside `reach-out` | @Luciver I can't attend the 5 PM stand-up because of a client call. | Records the excuse, posts a reach-out notice (with moderator @mention + embed) into the dedicated moderator channel only, and stores the excerpt for later stats. |
| *(any other message that includes the name)* | Luciver what can you do? | Falls back to the help embed so the user sees available actions. |

> Tip: Mentioning the bot (`@Luciver help`) behaves the same as typing its name.

## Automatic Behaviour

- **Greeting** – Responds with the welcome + code-of-conduct message when a user simply says `hi`, `hello`, or `luciver`.
- **Message capture** – Tracks all guild messages in `channelActivity` to power `stats` output.
- **Reminder engine** – Checks pending reminders every 30 seconds, DMs every targeted member at the scheduled time (supports @everyone and role fan-out), only falls back to the originating channel when a single-user DM fails, and records delivery in #luciver-log. Reminder confirmations and DMs include the configured timezone label so timestamps line up with human expectations, and default to 09:00 in that zone if you provide a date (or “tomorrow”) without a specific hour.
- **Daily progress prompt** – Every evening at 7 PM (configured timezone) DMs everyone in the `bashers` role with “Uploaded today's progress?! If not, do it now!!” and posts the delivery record to #luciver-log.
- **Weekly digest** – Each Sunday at 2 PM (configured timezone) lists all open assignments in the moderator channel and mirrors the post in #luciver-log (requires configuration).
- **Weekend pulse** – Each Sunday at 6 PM (configured timezone) posts the top-channel activity snapshot and current headcounts in #luciver-log for quick review.
- **Logging** – Every task creation, reminder creation, reminder delivery, and digest is echoed into the #luciver-log channel.
- **Voice session tracking** – Watches the `Voice Meeting` and `weekly-bash-discussion` voice channels, captures join durations, and posts attendance summaries to #luciver-log once the room clears out.
- **Reach-out tracking** – Any post in the configured `reach-out` channel that tags Luciver is sanitised, embedded, pushed to the moderator/log channels with a moderator role mention, acknowledged in-thread, and counted in the stats operations snapshot so moderators can monitor absences and excuses.
- **Insights layer** – Tracks per-channel and per-member message volume so `stats` calls can highlight top contributors, quiet channels, and pending operational items alongside role headcounts.
- **Startup health** – Logs `Luciver is online as ...` once the client connects so you know it is live.

## What You Can Tune

- **Reminder cadence** – Adjust `REMINDER_CHECK_INTERVAL_MS` if you need faster or slower sweeps.
- **Digest schedule** – Change `TASK_DIGEST_TARGET_DAY` / `TASK_DIGEST_TARGET_HOUR` for a different day or time; set `TASK_DIGEST_MIN_INTERVAL_MS` to avoid duplicate reports.
- **Local timezone** – Luciver defaults to Indian Standard Time (`Asia/Kolkata`). Provide `LUCIVER_TIMEZONE` (IANA format such as `America/New_York`) if you need a different zone so reminders, logs, and weekly reports render dates in your expected locale.
- **Moderator channel** – Provide `MODERATOR_CHANNEL_ID` in `.env` to enable weekly digests; leave empty to skip them.
- **Task permissions** – Only members with a role containing “moderator” can assign tasks through Luciver.
- **Reach-out channel name** – Override `REACH_OUT_CHANNEL_NAME` (defaults to `reach-out`) if your server uses a different channel slug for excuse submissions.

## Internal Stores

- `taskBacklog` – Array of open assignments (`status`, `lastNotifiedAt`, timestamps).
- `reminderQueue` – Array of reminders awaiting delivery plus timestamps and delivery outcomes.
- `channelActivity` – Map keyed by channel ID tracking counts and last active timestamps.
- `reachOutReports` – Rolling list (500 max) of reach-out notices with excerpts and timestamps for moderator insights and stats output.

## File Of Record

- `index.js` – Houses the Discord client configuration, message handlers, scheduling loops, and helper utilities.

## Setup & Run

1. Create `.env` with `TOKEN=<bot token>` and optionally `MODERATOR_CHANNEL_ID=<channel id>` / `LUCIVER_LOG_CHANNEL_ID=<channel id>`.
2. Install dependencies: `npm install`.
3. Launch: `node index.js`.
4. Validate in Discord using the triggers above.

## Future Optimisations

- Persist tasks and reminders so they survive restarts (database or JSON store).
- Add acknowledgement commands to mark tasks complete and skip them in the digest.
- Provide a slash-command layer mirroring the text cues for clearer autocomplete.

## Configuration Keys

- `TOKEN` – Discord bot token (required).
- `MODERATOR_CHANNEL_ID` – Channel used for the weekly digest (optional).
- `LUCIVER_LOG_CHANNEL_ID` – Channel that receives task/reminder logs (optional but recommended).
- `LUCIVER_TIMEZONE` – IANA timezone identifier (e.g. `Europe/London`) applied to reminder scheduling, digests, and log timestamps (defaults to `Asia/Kolkata`).
- `REACH_OUT_CHANNEL_NAME` – Lowercase name of the channel that collects excuse posts; defaults to `reach-out` if unset.
