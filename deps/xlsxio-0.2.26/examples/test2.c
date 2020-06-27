#include <stdlib.h>
#include <stdio.h>
#include <inttypes.h>
#include <string.h>
#include "xlsxio_read.h"

#define SAMPLE_PATH "../"

static const char* testfiles[] = {SAMPLE_PATH "test2.xlsx", SAMPLE_PATH "test2.xlsm", SAMPLE_PATH "test2.xltx", SAMPLE_PATH "test2.xltm"};

int sheet_row_callback (size_t row, size_t maxcol, void* callbackdata)
{
  printf("\n");
  return 0;
}

int sheet_cell_callback (size_t row, size_t col, const XLSXIOCHAR* value, void* callbackdata)
{
  struct xlsx_data* data = (struct xlsx_data*)callbackdata;
  if (col > 1)
    printf(",");
  if (value) {
    printf("%s", value);
  }
  return 0;
}

int print_sheet (char* name, void* callbackdata)
{
  printf("-[%s]-\n", name);
  xlsxioread_process((xlsxioreader)callbackdata, name, XLSXIOREAD_SKIP_EMPTY_ROWS, sheet_cell_callback, sheet_row_callback, NULL);
}

int main (int argc, char* argv[])
{
  int i;
  xlsxioreader handle;
  for (i = 0; i < sizeof(testfiles) / sizeof(*testfiles); i++) {
    printf("[%s]\n", testfiles[i]);
    if ((handle = xlsxioread_open(testfiles[i])) == NULL) {
      fprintf(stderr, "ERROR: failed to open %s\n", testfiles[i]);
    } else {
      xlsxioread_list_sheets(handle, print_sheet, handle);

      xlsxioread_close(handle);
    }
  }
  return 0;
}
