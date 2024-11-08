import math
from dataclasses import dataclass
from pathlib import Path

from astropy.io import fits
from astropy.io.fits import Header, ImageHDU, BinTableHDU

HDR_LOC = "hdrLoc"
DATA_LOC = "datLoc"


@dataclass
class Display_Array3D:
    local_identifier_reference: str

    def to_str(self):
        return f"""
        <disp:Display_Settings>
            <Local_Internal_Reference>
                <local_identifier_reference>{self.local_identifier_reference}</local_identifier_reference>
                <local_reference_type>display_settings_to_array</local_reference_type>
            </Local_Internal_Reference>
            <disp:Display_Direction>
                <disp:horizontal_display_axis>Third</disp:horizontal_display_axis>
                <disp:horizontal_display_direction>Left to Right</disp:horizontal_display_direction>
                <disp:vertical_display_axis>Sample</disp:vertical_display_axis>
                <disp:vertical_display_direction>Bottom to Top</disp:vertical_display_direction>
            </disp:Display_Direction>
        </disp:Display_Settings>
        """


@dataclass
class Header_PDS4:
    # <name>Image Header 2 DC</name>
    #    <local_identifier>image_2_hdu</local_identifier>
    #    <offset unit="byte">9503616</offset>
    #    <object_length unit="byte">2880</object_length>
    name: str
    local_id: str
    byte_offset: int
    byte_len: int

    def to_str(self) -> str:
        return f"""
        <Header>
         <name>{self.name}</name>
            <local_identifier>{self.local_id}</local_identifier>
            <offset unit="byte">{self.byte_offset}</offset>
            <object_length unit="byte">{self.byte_len}</object_length>
            
            <parsing_standard_id>FITS 4.0</parsing_standard_id>
        </Header>
        """


@dataclass
class Axis:
    #     <axis_name>Line</axis_name>
    #          <elements>332</elements>
    #          <sequence_number>1</sequence_number>
    axis_name: str
    elements: int
    sequence_number: int


@dataclass
class Array3D:
    # <name>WAVELENGTHS</name>
    # <local_identifier>image_dc</local_identifier>
    # <offset unit="byte">9506496</offset>
    # <axes>3</axes>
    # <axis_index_order>Last Index Fastest</axis_index_order>
    # <Element_Array>
    #    <data_type>ComplexMSB16</data_type>
    # </Element_Array>
    name: str
    lid: str
    data_type: str
    offset: int
    axes: list[Axis]

    def to_str(self):
        return f"""
        <Array_3D_Image>
        <name>{self.name}</name>
          <local_identifier>{self.lid}</local_identifier>
          <offset unit="byte">{self.offset}</offset>
          <axes>3</axes>
          <axis_index_order>Last Index Fastest</axis_index_order>
          <Element_Array>
             <data_type>{self.data_type}</data_type>
          </Element_Array>
          {self.get_axes_str()}
        </Array_3D_Image>
        """

    def get_axes_str(self) -> str:
        axes = ""

        for axis in sorted(self.axes, key=lambda x: x.sequence_number):
            axes += f"""
            <Axis_Array>
             <axis_name>{axis.axis_name}</axis_name>
             <elements>{axis.elements}</elements>
             <sequence_number>{axis.sequence_number}</sequence_number>
          </Axis_Array>
            """
        return axes

    def get_byte_size(self) -> int:
        """
        TODO use data type
        :return:
        """
        return 4 * self.axes[0].elements * self.axes[1].elements * self.axes[2].elements


FITS_HEADER_BLOCK_SIZE = 2880
FITS_CARDS_PER_BLOCK = 36


def block_number_to_header_size(blocks: int) -> int:
    return blocks * FITS_HEADER_BLOCK_SIZE


def get_block_number(file_or_header: Path | str | Header) -> int:
    if isinstance(file_or_header, (Path, str)):
        fits_file = Path(file_or_header)
        header = fits.getheader(fits_file)
    elif isinstance(file_or_header, Header):
        header = file_or_header
    else:
        raise ValueError("file_or_header should be a Path or a Header")
    card_number = len(header.cards)
    card_number_with_end_keyword = card_number + 1  # Add the END keyword
    number_of_card_per_block = FITS_CARDS_PER_BLOCK
    block_number = math.ceil(card_number_with_end_keyword / number_of_card_per_block)
    return block_number


def get_header_size(file_or_header: Path | str | Header) -> int:
    blocks = get_block_number(file_or_header)
    header_size = block_number_to_header_size(blocks)
    return header_size


def get_header(hdu: ImageHDU) -> Header_PDS4:
    header = hdu.header
    file_info = hdu.fileinfo()
    header_offset = file_info[HDR_LOC]
    data_offset = file_info[DATA_LOC]
    header_len = header_offset - data_offset
    header = Header_PDS4(name=header.get("EXTNAME"), local_id=header.get("EXTNAME").lower(), byte_offset=header_offset,
                         byte_len=header_len

                         )
    return header


def get_array_3d(hdu: ImageHDU) -> Array3D:
    header = hdu.header
    file_info = hdu.fileinfo()
    offset = file_info[DATA_LOC]
    naxis1 = header.get("NAXIS1")
    naxis2 = header.get("NAXIS2")
    naxis3 = header.get("NAXIS3")
    axis1 = Axis(axis_name="Line", elements=naxis3, sequence_number=1, )
    axis2 = Axis(axis_name="Sample", elements=naxis2, sequence_number=2, )
    axis3 = Axis(axis_name="Third", elements=naxis1, sequence_number=3)
    data_type_h = header.get('BITPIX')
    if data_type_h == -32:
        data_type = "IEEE754MSBSingle"
        # see https://sbnwiki.asteroiddata.org/Notes_for_Labelling_FITS_files.html
    else:
        raise RuntimeError(f"Unsuported data_type {data_type_h}")

    array_3d = Array3D(name=f"array_{header.get('EXTNAME')}", lid=f"array_{header.get('EXTNAME').lower()}",
                       data_type=data_type, axes=[axis1, axis2, axis3], offset=offset, )

    return array_3d


def is_array3d(header: Header) -> bool:
    if header.get("NAXIS3"):
        return True
    return False


@dataclass
class GeneratedContent:
    file_area_content: str
    display_content: str


def get_table_pds4(hdu: BinTableHDU) -> str:
    header = hdu.header
    columns = hdu.columns


def get_content(fits_file_path: str | Path) -> GeneratedContent:
    fits_file_path = Path(fits_file_path)
    hdul = fits.open(fits_file_path)
    content = ""
    display = ""
    for hdu in hdul:
        if is_array3d(hdu.header):
            header = get_header(hdu)
            content += f"\n{header.to_str()}\n"
            array = get_array_3d(hdu)
            content += f"\n{array.to_str()}\n"
            display += Display_Array3D(local_identifier_reference=array.lid).to_str()
        elif isinstance(hdu, BinTableHDU):
            header = get_header(hdu)
            content += f"\n{header.to_str()}\n"
            table = get_table_pds4(hdu)
            content += f"\n{table}\n"
            

    file_area_content = f"""
      <File_Area_Observational>
       <File>
          <file_name>{fits_file_path.name}</file_name>
       </File>
       {content}
       </File_Area_Observational>
    """""

    return GeneratedContent(file_area_content=file_area_content, display_content=display)


if __name__ == '__main__':
    content = get_content("fits_binary_tables.fits")
    template = Path("fits_binary_table_template.xml")
    file = Path("fits_binary_tables.xml")
    file.unlink(missing_ok=True)
    file.touch()
    template_txt = template.read_text()
    template_txt = template_txt.replace("</File_Area_Observational>", content.file_area_content)
    template_txt = template_txt.replace("</Display_Settings>", content.display_content)
    file.write_text(template_txt)
