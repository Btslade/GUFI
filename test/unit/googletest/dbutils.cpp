/*
This file is part of GUFI, which is part of MarFS, which is released
under the BSD license.


Copyright (c) 2017, Los Alamos National Security (LANS), LLC
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation and/or
other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors
may be used to endorse or promote products derived from this software without
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


From Los Alamos National Security, LLC:
LA-CC-15-039

Copyright (c) 2017, Los Alamos National Security, LLC All rights reserved.
Copyright 2017. Los Alamos National Security, LLC. This software was produced
under U.S. Government contract DE-AC52-06NA25396 for Los Alamos National
Laboratory (LANL), which is operated by Los Alamos National Security, LLC for
the U.S. Department of Energy. The U.S. Government has rights to use,
reproduce, and distribute this software.  NEITHER THE GOVERNMENT NOR LOS
ALAMOS NATIONAL SECURITY, LLC MAKES ANY WARRANTY, EXPRESS OR IMPLIED, OR
ASSUMES ANY LIABILITY FOR THE USE OF THIS SOFTWARE.  If software is
modified to produce derivative works, such modified software should be
clearly marked, so as not to confuse it with the version available from
LANL.

THIS SOFTWARE IS PROVIDED BY LOS ALAMOS NATIONAL SECURITY, LLC AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL LOS ALAMOS NATIONAL SECURITY, LLC OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY
OF SUCH DAMAGE.
*/



#include <ctime>
#include <grp.h>
#include <pwd.h>
#include <sys/types.h>
#include <unistd.h>

#include <gtest/gtest.h>

extern "C" {

#include "dbutils.h"

}

static int str_output(void *args, int, char **data, char **) {
    char *output = static_cast <char *> (args);
    const size_t len = strlen(data[0]);
    memcpy(output, data[0], len);
    output[len] = '\0';
    return 0;
}

TEST(create_table_wrapper, nullptr) {
    EXPECT_NE(create_table_wrapper(nullptr, nullptr, nullptr, nullptr), SQLITE_OK);
}

TEST(set_db_pragmas, good) {
    sqlite3 *db = NULL;
    ASSERT_EQ(sqlite3_open_v2(":memory:", &db, SQLITE_OPEN_READWRITE | SQLITE_OPEN_CREATE | SQLITE_OPEN_URI, NULL), SQLITE_OK);
    EXPECT_EQ(set_db_pragmas(db), 0);
    EXPECT_EQ(sqlite3_close(db), SQLITE_OK);
}

TEST(set_db_pragmas, nullptr) {
    EXPECT_EQ(set_db_pragmas(nullptr), 1);
}

TEST(addqueryfuncs, path) {
    const char dirname[MAXPATH] = "dirname";

    struct work work;
    memset(&work, 0, sizeof(work));
    work.root_parent.data = "index_root";     // currently at this path
    work.root_parent.len = strlen(work.root_parent.data);
    work.name_len = SNPRINTF(work.name, MAXPATH, "%s/%s", work.root_parent.data, dirname);

    sqlite3 *db = nullptr;
    ASSERT_EQ(sqlite3_open(":memory:", &db), SQLITE_OK);
    ASSERT_NE(db, nullptr);
    ASSERT_EQ(addqueryfuncs(db, 0, &work), 0);

    char output[MAXPATH] = {};
    EXPECT_EQ(sqlite3_exec(db, "SELECT path();", str_output, output, nullptr), SQLITE_OK);

    EXPECT_STREQ(output, work.name);

    sqlite3_close(db);
}

TEST(addqueryfuncs, epath) {
    const char dirname[MAXPATH] = "dirname";

    struct work work;
    memset(&work, 0, sizeof(work));
    work.root_parent.data = "index_root";     // currently at this path
    work.root_parent.len = strlen(work.root_parent.data);
    work.name_len = SNPRINTF(work.name, MAXPATH, "%s/%s", work.root_parent.data, dirname);
    work.basename_len = strlen(dirname);

    sqlite3 *db = nullptr;
    ASSERT_EQ(sqlite3_open(":memory:", &db), SQLITE_OK);
    ASSERT_NE(db, nullptr);
    ASSERT_EQ(addqueryfuncs(db, 0, &work), 0);

    char output[MAXPATH] = {};
    EXPECT_EQ(sqlite3_exec(db, "SELECT epath();", str_output, output, nullptr), SQLITE_OK);

    EXPECT_STREQ(output, dirname);

    sqlite3_close(db);
}

TEST(addqueryfuncs, rpath) {
    const char dirname[MAXPATH] = "dirname";

    struct work work;
    memset(&work, 0, sizeof(work));
    work.root_parent.data = "index_root";     // currently at this path
    work.root_parent.len = strlen(work.root_parent.data);
    work.name_len = SNPRINTF(work.name, MAXPATH, "%s/%s", work.root_parent.data, dirname);

    sqlite3 *db = nullptr;
    ASSERT_EQ(sqlite3_open(":memory:", &db), SQLITE_OK);
    ASSERT_NE(db, nullptr);
    ASSERT_EQ(addqueryfuncs(db, 0, &work), 0);

    for(int rollupscore : {0, 1}) {
        char query[MAXSQL] = {};
        SNPRINTF(query, MAXSQL, "SELECT rpath(\"%s\", %d);", dirname, rollupscore);

        // the path returned by the query is the path without the index prefix
        char output[MAXPATH] = {};
        EXPECT_EQ(sqlite3_exec(db, query, str_output, output, nullptr), SQLITE_OK);

        EXPECT_STREQ(output, dirname);
    }

    sqlite3_close(db);
}

TEST(addqueryfuncs, uidtouser) {
    // user caller's uid
    const uid_t uid = getuid();

    struct passwd pwd;
    struct passwd *result = NULL;

    char buf[MAXPATH] = {};
    ASSERT_EQ(getpwuid_r(uid, &pwd, buf, MAXPATH, &result), 0);
    ASSERT_EQ(result, &pwd);

    sqlite3 *db = nullptr;
    ASSERT_EQ(sqlite3_open(":memory:", &db), SQLITE_OK);
    ASSERT_NE(db, nullptr);

    ASSERT_EQ(addqueryfuncs_common(db), 0);

    // use value obtained from summary table
    char query[MAXSQL] = {};
    SNPRINTF(query, MAXSQL, "SELECT uidtouser('%d')", uid);

    char output[MAXPATH] = {};
    ASSERT_EQ(sqlite3_exec(db, query, str_output, output, NULL), SQLITE_OK);

    EXPECT_STREQ(output, pwd.pw_name);

    sqlite3_close(db);
}

TEST(addqueryfuncs, gidtogroup) {
    // user caller's gid
    const gid_t gid = getgid();

    struct group grp;
    struct group *result = NULL;

    char buf[MAXPATH] = {};
    ASSERT_EQ(getgrgid_r(gid, &grp, buf, MAXPATH, &result), 0);
    ASSERT_EQ(result, &grp);

    sqlite3 *db = nullptr;
    ASSERT_EQ(sqlite3_open(":memory:", &db), SQLITE_OK);
    ASSERT_NE(db, nullptr);

    ASSERT_EQ(addqueryfuncs_common(db), 0);

    // use value obtained from summary table
    char query[MAXSQL] = {};
    SNPRINTF(query, MAXSQL, "SELECT gidtogroup('%d')", gid);

    char output[MAXPATH] = {};
    ASSERT_EQ(sqlite3_exec(db, query, str_output, output, NULL), SQLITE_OK);

    EXPECT_STREQ(output, grp.gr_name);

    sqlite3_close(db);
}

TEST(addqueryfuncs, modetotxt) {
    sqlite3 *db = nullptr;
    ASSERT_EQ(sqlite3_open(":memory:", &db), SQLITE_OK);
    ASSERT_NE(db, nullptr);

    ASSERT_EQ(addqueryfuncs_common(db), 0);

    for(mode_t perm = 0; perm < 01000; perm++) {
        char query[MAXSQL] = {};
        char output[11] = {};
        char expected[11] = {};

        // file
        SNPRINTF(query, MAXSQL, "SELECT modetotxt(%zu)", (size_t) perm);
        ASSERT_EQ(sqlite3_exec(db, query, str_output, output, NULL), SQLITE_OK);
        EXPECT_STREQ(output, modetostr(expected, 11, perm));

        // directory
        SNPRINTF(query, MAXSQL, "SELECT modetotxt(%zu)", perm | S_IFDIR);
        ASSERT_EQ(sqlite3_exec(db, query, str_output, output, NULL), SQLITE_OK);
        EXPECT_STREQ(output, modetostr(expected, 11, perm | S_IFDIR));
    }

    sqlite3_close(db);
}

TEST(addqueryfuncs, strftime) {
    sqlite3 *db = nullptr;
    ASSERT_EQ(sqlite3_open(":memory:", &db), SQLITE_OK);
    ASSERT_NE(db, nullptr);

    ASSERT_EQ(addqueryfuncs_common(db), 0);

    const char fmt[] = "%a %A %b %B %c %C %d %D %e %F %g %G %h %H %I %j %m %M %n %p %r %R %S %t %T %u %U %V %w %W %x %X %y %Y %z %Z %%";

    const time_t now = time(nullptr);

    char query[MAXSQL] = {};
    SNPRINTF(query, MAXSQL, "SELECT strftime('%s', %d)", fmt, (int) now);

    char output[MAXPATH] = {};
    ASSERT_EQ(sqlite3_exec(db, query, str_output, output, NULL), SQLITE_OK);

    char expected[MAXSQL] = {};
    struct tm tm;
    ASSERT_NE(localtime_r(&now, &tm), nullptr);
    EXPECT_NE(strftime(expected, MAXSQL, fmt, &tm), (size_t) 0);

    EXPECT_STREQ(output, expected);

    sqlite3_close(db);
}

static const char SIZE[] = {'K',    // 10
                            'M',    // 20
                            'G',    // 30
                            'T',    // 40
                            'P',    // 50
                            'E',    // 60
                            // 'Z', // 70
                            // 'Y'  // 80
};

TEST(addqueryfuncs, blocksize) {
    sqlite3 *db = nullptr;
    ASSERT_EQ(sqlite3_open(":memory:", &db), SQLITE_OK);
    ASSERT_NE(db, nullptr);

    ASSERT_EQ(addqueryfuncs_common(db), 0);

    const char expecteds[] = {'1', '1', '2'};

    size_t Bsize = 1;
    size_t iBsize = 1;
    for(size_t i = 0; i < sizeof(SIZE); i++) {
        Bsize  *= 1000;
        const size_t Binputs[] = {
            Bsize - 1,
            Bsize,
            Bsize + 1
        };

        iBsize *= 1024;
        const size_t iBinputs[] = {
            iBsize - 1,
            iBsize,
            iBsize + 1
        };

        for(size_t j = 0; j < 3; j++) {
            char query[MAXSQL] = {};
            char output[MAXPATH] = {};
            char expected[MAXPATH] = {};

            SNPRINTF(query, MAXSQL, "SELECT blocksize(%zu, '%c')", iBinputs[j], SIZE[i]);
            ASSERT_EQ(sqlite3_exec(db, query, str_output, output, NULL), SQLITE_OK);
            SNPRINTF(expected, MAXPATH, "%c%c", expecteds[j], SIZE[i]);
            EXPECT_STREQ(output, expected);

            SNPRINTF(query, MAXSQL, "SELECT blocksize(%zu, '%cB')", Binputs[j], SIZE[i]);
            ASSERT_EQ(sqlite3_exec(db, query, str_output, output, NULL), SQLITE_OK);
            SNPRINTF(expected, MAXPATH, "%c%cB", expecteds[j], SIZE[i]);
            EXPECT_STREQ(output, expected);

            SNPRINTF(query, MAXSQL, "SELECT blocksize(%zu, '%ciB')", iBinputs[j], SIZE[i]);
            ASSERT_EQ(sqlite3_exec(db, query, str_output, output, NULL), SQLITE_OK);
            SNPRINTF(expected, MAXPATH, "%c%ciB", expecteds[j], SIZE[i]);
            EXPECT_STREQ(output, expected);
        }
    }

    sqlite3_close(db);
}

TEST(addqueryfuncs, human_readable_size) {
    sqlite3 *db = nullptr;
    ASSERT_EQ(sqlite3_open(":memory:", &db), SQLITE_OK);
    ASSERT_NE(db, nullptr);

    ASSERT_EQ(addqueryfuncs_common(db), 0);

    char query[MAXSQL] = {};
    char output[MAXPATH] = {};

    size_t size = 1;

    SNPRINTF(query, MAXSQL, "SELECT human_readable_size(%zu)", size);
    ASSERT_EQ(sqlite3_exec(db, query, str_output, output, NULL), SQLITE_OK);
    EXPECT_STREQ(output, "1.0");

    // greater than 1K - has unit suffix
    for(size_t i = 0; i < sizeof(SIZE); i++) {
        char expected[MAXPATH] = {};

        size *= 1024;

        SNPRINTF(query, MAXSQL, "SELECT human_readable_size(%zu)", size + (size / 10));
        ASSERT_EQ(sqlite3_exec(db, query, str_output, output, NULL), SQLITE_OK);
        SNPRINTF(expected, MAXPATH, "1.1%c", SIZE[i]);
        EXPECT_STREQ(output, expected);
    }

    sqlite3_close(db);
}

TEST(addqueryfuncs, level) {
    struct work work;
    memset(&work, 0, sizeof(work));

    sqlite3 *db = nullptr;
    ASSERT_EQ(sqlite3_open(":memory:", &db), SQLITE_OK);
    ASSERT_NE(db, nullptr);

    for(work.level = 0; work.level < 10; work.level++) {
        ASSERT_EQ(addqueryfuncs(db, 0, &work), 0);

        char output[MAXPATH] = {};
        ASSERT_EQ(sqlite3_exec(db, "SELECT level()", str_output, output, NULL), SQLITE_OK);

        char expected[MAXPATH] = {};
        SNPRINTF(expected, MAXPATH, "%zu", work.level);

        EXPECT_STREQ(output, expected);
    }

    sqlite3_close(db);
}

TEST(addqueryfuncs, starting_point) {
    struct work work;
    memset(&work, 0, sizeof(work));
    work.root_parent.data = "/index_root";

    sqlite3 *db = nullptr;
    ASSERT_EQ(sqlite3_open(":memory:", &db), SQLITE_OK);
    ASSERT_NE(db, nullptr);

    ASSERT_EQ(addqueryfuncs(db, 0, &work), 0);

    char output[MAXPATH] = {};
    ASSERT_EQ(sqlite3_exec(db, "SELECT starting_point()", str_output, output, NULL), SQLITE_OK);

    EXPECT_STREQ(output, work.root_parent.data);

    sqlite3_close(db);
}

TEST(addqueryfuncs, basename) {
    sqlite3 *db = nullptr;
    ASSERT_EQ(sqlite3_open(":memory:", &db), SQLITE_OK);
    ASSERT_NE(db, nullptr);

    ASSERT_EQ(addqueryfuncs_common(db), 0);

    char output[MAXPATH] = {};

    /* from basename(3) manpage */

    ASSERT_EQ(sqlite3_exec(db, "SELECT basename('/usr/lib')", str_output, output, NULL), SQLITE_OK);
    EXPECT_STREQ(output, "lib");

    ASSERT_EQ(sqlite3_exec(db, "SELECT basename('/usr/')", str_output, output, NULL), SQLITE_OK);
    EXPECT_STREQ(output, "usr");

    ASSERT_EQ(sqlite3_exec(db, "SELECT basename('usr')", str_output, output, NULL), SQLITE_OK);
    EXPECT_STREQ(output, "usr");

    ASSERT_EQ(sqlite3_exec(db, "SELECT basename('/')", str_output, output, NULL), SQLITE_OK);
    EXPECT_STREQ(output, "/");

    ASSERT_EQ(sqlite3_exec(db, "SELECT basename('.')", str_output, output, NULL), SQLITE_OK);
    EXPECT_STREQ(output, ".");

    ASSERT_EQ(sqlite3_exec(db, "SELECT basename('..')", str_output, output, NULL), SQLITE_OK);
    EXPECT_STREQ(output, "..");

    sqlite3_close(db);
}

TEST(sqlite_uri_path, 23) {
    const char src[] = "prefix/#/basename";
    size_t src_len = strlen(src);
    char dst[1024] = {0};
    const char expected[] = "prefix/%23/basename";

    const size_t dst_len = sqlite_uri_path(dst, sizeof(dst), src, &src_len);

    EXPECT_EQ(src_len, strlen(src));
    EXPECT_EQ(dst_len, strlen(expected));
    EXPECT_STREQ(dst, expected);
}

TEST(sqlite_uri_path, 3f) {
    const char src[] = "prefix/?/basename";
    size_t src_len = strlen(src);
    char dst[1024] = {0};
    const char expected[] = "prefix/%3f/basename";

    const size_t dst_len = sqlite_uri_path(dst, sizeof(dst), src, &src_len);

    EXPECT_EQ(src_len, strlen(src));
    EXPECT_EQ(dst_len, strlen(expected));
    EXPECT_STREQ(dst, expected);
}

TEST(sqlite_uri_path, not_enough_space) {
    const char src[] = "prefix/#/basename";

    // does not hit conversion
    {
        size_t src_len = strlen(src);
        char dst[7] = {0};
        const char expected[] = "prefix/";

        const size_t dst_len = sqlite_uri_path(dst, sizeof(dst), src, &src_len);

        EXPECT_EQ(src_len, (size_t) 7); // prefix/
        EXPECT_EQ(dst_len, strlen(expected));
        EXPECT_EQ(memcmp(expected, dst, dst_len), 0);
    }

    // # -> %
    {
        size_t src_len = strlen(src);
        char dst[8] = {0};
        const char expected[] = "prefix/%";

        const size_t dst_len = sqlite_uri_path(dst, sizeof(dst), src, &src_len);

        EXPECT_EQ(src_len, (size_t) 8); // prefix/#
        EXPECT_EQ(dst_len, strlen(expected));
        EXPECT_EQ(memcmp(expected, dst, dst_len), 0);
    }

    // # -> %2
    {
        size_t src_len = strlen(src);
        char dst[9] = {0};
        const char expected[] = "prefix/%2";

        const size_t dst_len = sqlite_uri_path(dst, sizeof(dst), src, &src_len);

        EXPECT_EQ(src_len, (size_t) 8); // prefix/#
        EXPECT_EQ(dst_len, strlen(expected));
        EXPECT_EQ(memcmp(expected, dst, dst_len), 0);
    }
}
